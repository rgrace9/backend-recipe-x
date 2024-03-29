"""empty message

Revision ID: 7f90902c8773
Revises: 
Create Date: 2024-02-20 14:39:05.688954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f90902c8773'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allergy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ingredient_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['ingredient_category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ingredient_allergy',
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.Column('allergy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['allergy_id'], ['allergy.id'], ),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ),
    sa.PrimaryKeyConstraint('ingredient_id', 'allergy_id')
    )
    op.create_table('ingredient_diet',
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.Column('diet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['diet_id'], ['diet.id'], ),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ),
    sa.PrimaryKeyConstraint('ingredient_id', 'diet_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ingredient_diet')
    op.drop_table('ingredient_allergy')
    op.drop_table('ingredient')
    op.drop_table('ingredient_category')
    op.drop_table('diet')
    op.drop_table('allergy')
    # ### end Alembic commands ###
