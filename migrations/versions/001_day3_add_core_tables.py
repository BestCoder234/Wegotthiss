"""day3 add core tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create prices_eod table
    op.create_table('prices_eod',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('trade_date', sa.Date(), nullable=False),
        sa.Column('open', sa.Float(), nullable=False),
        sa.Column('high', sa.Float(), nullable=False),
        sa.Column('low', sa.Float(), nullable=False),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prices_eod_symbol'), 'prices_eod', ['symbol'], unique=False)
    op.create_index(op.f('ix_prices_eod_trade_date'), 'prices_eod', ['trade_date'], unique=False)
    
    # Create fundamentals table
    op.create_table('fundamentals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('fiscal_year', sa.Integer(), nullable=False),
        sa.Column('eps', sa.Float(), nullable=False),
        sa.Column('book_value', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fundamentals_symbol'), 'fundamentals', ['symbol'], unique=False)


def downgrade() -> None:
    # Drop fundamentals table
    op.drop_index(op.f('ix_fundamentals_symbol'), table_name='fundamentals')
    op.drop_table('fundamentals')
    
    # Drop prices_eod table
    op.drop_index(op.f('ix_prices_eod_trade_date'), table_name='prices_eod')
    op.drop_index(op.f('ix_prices_eod_symbol'), table_name='prices_eod')
    op.drop_table('prices_eod') 