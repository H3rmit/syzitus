"""empty message

Revision ID: 8328d5cb4e97
Revises: 5f7397245f89
Create Date: 2022-12-12 10:50:46.287311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import FetchedValue


# revision identifiers, used by Alembic.
revision = '8328d5cb4e97'
down_revision = '5f7397245f89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('save_relationship')
    op.create_index(op.f('ix_commentvotes_comment_id'), 'commentvotes', ['comment_id'], unique=False)
    op.create_index(op.f('ix_votes_submission_id'), 'votes', ['submission_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_votes_submission_id'), table_name='votes')
    op.drop_index(op.f('ix_commentvotes_comment_id'), table_name='commentvotes')
    op.create_table('save_relationship',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('submission_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], name='save_relationship_submission_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='save_relationship_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='save_relationship_pkey')
    )
    # ### end Alembic commands ###
