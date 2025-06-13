from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


class Project(Base):
    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    name: Mapped[str] = mapped_column(String(length=50))
    main_domains: Mapped[list["MainDomain"]] = relationship(back_populates="project")
    regex_exclusions: Mapped[list["RegexExclusion"]] = relationship(
        back_populates="project"
    )


class MainDomain(Base):
    domain: Mapped[str] = mapped_column(String(length=256))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    project: Mapped["Project"] = relationship(back_populates="main_domains")


# class UtilNameSettings(Base):
