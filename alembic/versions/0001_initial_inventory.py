"""initial inventory schema

Revision ID: 0001
Revises:
Create Date: 2026-09-21
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(128), unique=True, nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "suppliers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("code", sa.String(64), unique=True, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("email", sa.String(256)),
        sa.Column("phone", sa.String(64)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "warehouses",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("code", sa.String(32), unique=True, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("region", sa.String(64), server_default="US"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "skus",
        sa.Column("sku", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("category_id", sa.String(36), sa.ForeignKey("categories.id")),
        sa.Column("supplier_id", sa.String(36), sa.ForeignKey("suppliers.id")),
        sa.Column("unit_cost_cents", sa.Integer(), server_default="0"),
        sa.Column("status", sa.String(32), server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "stock_levels",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("sku", sa.String(64), sa.ForeignKey("skus.sku"), nullable=False),
        sa.Column("warehouse_id", sa.String(36), sa.ForeignKey("warehouses.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="0"),
        sa.Column("reserved", sa.Integer(), server_default="0"),
        sa.UniqueConstraint("sku", "warehouse_id", name="uq_stock_sku_wh"),
    )
    op.create_table(
        "reservations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("sku", sa.String(64), sa.ForeignKey("skus.sku"), nullable=False),
        sa.Column("warehouse_id", sa.String(36), sa.ForeignKey("warehouses.id"), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(32), server_default="held"),
        sa.Column("order_ref", sa.String(64)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "stock_movements",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("sku", sa.String(64), nullable=False),
        sa.Column("warehouse_id", sa.String(36), nullable=False),
        sa.Column("delta", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(64), nullable=False),
        sa.Column("meta", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    for t in (
        "stock_movements",
        "reservations",
        "stock_levels",
        "skus",
        "warehouses",
        "suppliers",
        "categories",
    ):
        op.drop_table(t)
