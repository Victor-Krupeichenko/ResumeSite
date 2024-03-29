"""migrate_3

Revision ID: 96a08f522982
Revises: a52aa6bc9ff9
Create Date: 2024-02-05 01:49:58.065259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96a08f522982'
down_revision: Union[str, None] = 'a52aa6bc9ff9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('experience', 'year_finish',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('experience', 'year_finish',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
