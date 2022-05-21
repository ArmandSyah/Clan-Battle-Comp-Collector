"""empty message

Revision ID: de3102522b85
Revises: 6e60c8e207e4
Create Date: 2022-05-21 18:21:36.208405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de3102522b85'
down_revision = '6e60c8e207e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('unit_id', sa.Integer(), nullable=False),
    sa.Column('unit_name', sa.String(length=80), nullable=False),
    sa.Column('unit_name_en', sa.String(length=80), nullable=False),
    sa.Column('thematic', sa.String(length=80), nullable=True),
    sa.Column('thematic_en', sa.String(length=80), nullable=True),
    sa.Column('range', sa.Integer(), nullable=False),
    sa.Column('icon', sa.String(length=200), nullable=False),
    sa.Column('max_star', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('icon'),
    sa.UniqueConstraint('unit_id')
    )
    op.create_table('clan_battle',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('clan_battle_id', sa.Integer(), nullable=False),
    sa.Column('training_start_date', sa.DateTime(), nullable=False),
    sa.Column('training_end_date', sa.DateTime(), nullable=False),
    sa.Column('main_start_date', sa.DateTime(), nullable=False),
    sa.Column('main_end_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('clan_battle_id')
    )
    op.create_table('boss',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('unit_id', sa.Integer(), nullable=False),
    sa.Column('unit_name', sa.String(length=80), nullable=False),
    sa.Column('unit_name_en', sa.String(length=80), nullable=False),
    sa.Column('icon', sa.String(length=200), nullable=False),
    sa.Column('clan_battle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clan_battle_id'], ['clan_battle.clan_battle_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team_comp',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('video_url', sa.String(length=200), nullable=True),
    sa.Column('expected_damage', sa.BigInteger(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('phase', sa.Integer(), nullable=False),
    sa.Column('playstyle', sa.String(length=80), nullable=False),
    sa.Column('boss_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['boss_id'], ['boss.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team_comp_character',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('ue', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('team_comp_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.unit_id'], ),
    sa.ForeignKeyConstraint(['team_comp_id'], ['team_comp.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_comp_character')
    op.drop_table('team_comp')
    op.drop_table('boss')
    op.drop_table('clan_battle')
    op.drop_table('character')
    # ### end Alembic commands ###
