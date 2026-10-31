from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (CheckConstraint, DateTime, ForeignKey, String,
                        false, func, true)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[str] = mapped_column(String(20), default="visitor",
                                      server_default="visitor")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("role IN ('visitor', 'staff')", name="ck_users_role"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    active: Mapped[bool] = mapped_column(default=True, server_default=true())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="waiting",
                                        server_default="waiting")
    court: Mapped[int | None] = mapped_column()
    open_to_singles: Mapped[bool] = mapped_column(default=False,
                                                  server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")
    members: Mapped[list["TicketMember"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan",
        passive_deletes=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status"),
        CheckConstraint(
            "court IS NULL OR (court BETWEEN 1 AND 3 AND status = 'called')",
            name="ck_tickets_court"),
    )

    @property
    def players(self):
        """Computed, not stored: the owner plus the listed members."""
        return 1 + len(self.members)


class TicketMember(db.Model):
    __tablename__ = "ticket_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(80))

    ticket: Mapped["Ticket"] = relationship(back_populates="members")