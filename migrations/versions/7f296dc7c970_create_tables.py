"""create tables

Revision ID: 7f296dc7c970
Revises: 
Create Date: 2023-05-11 16:15:09.139864

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import MONEY

# revision identifiers, used by Alembic.
revision = '7f296dc7c970'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("first_name", sa.String(length=25), nullable=False),
        sa.Column("last_name", sa.String(length=25), nullable=False),
        sa.Column("role", sa.Enum("BUYER", "SELLER", name="user_roles"), nullable=False),
    )
    op.create_table(
        "flowers",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("type", sa.String(length=100), nullable=False),
    )
    op.create_table(
        "shades",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("color", sa.String(length=7), nullable=False),
    )
    op.create_table(
        "flower_shades",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("flower_id", sa.Integer, sa.ForeignKey("flowers.id"), nullable=False),
        sa.Column("shade_id", sa.SmallInteger, sa.ForeignKey("shades.id"), nullable=False),
    )
    op.create_table(
        "flower_prices",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("flower_id", sa.Integer, sa.ForeignKey("flowers.id"), nullable=False),
        sa.Column("price", MONEY, nullable=False),
        sa.Column("start_date", sa.Date, server_default=sa.text("NOW()::DATE")),
        sa.Column("end_date", sa.Date, server_default=sa.text("'2999-12-31'::DATE")),
    )
    op.create_table(
        "flower_amounts",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("flower_id", sa.Integer, sa.ForeignKey("flowers.id"), nullable=False),
        sa.Column("sign", sa.Boolean, server_default=sa.text("true")),
        sa.Column("amount", sa.Integer),
        sa.Column("active_date", sa.Date, server_default=sa.text("NOW()::DATE")),
    )
    op.create_table(
        "lots",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("flower_id", sa.Integer, sa.ForeignKey("flowers.id"), nullable=False),
        sa.Column("seller_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
    )
    op.create_table(
        "deals",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("lot_id", sa.Integer, sa.ForeignKey("lots.id"), nullable=False),
        sa.Column("buyer_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("executed_date", sa.Date, server_default=sa.text("NOW()::DATE")),
        sa.Column("amount", sa.Integer),
    )
    op.create_table(
        "flower_reviews",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("lot_id", sa.Integer, sa.ForeignKey("lots.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
    )
    op.create_table(
        "seller_reviews",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("buyer_id", sa.Integer, sa.ForeignKey("lots.id"), nullable=False),
        sa.Column("seller_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
    )
    
def downgrade() -> None:
    pass
