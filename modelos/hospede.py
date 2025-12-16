from __future__ import annotations
import sqlite3
from persistencia.dados import get_db


class Hospede:
    def __init__(self, nome="", documento="", email="", telefone="", id=None):
        self.id = id
        self.nome = nome
        self.documento = documento
        self.email = email
        self.telefone = telefone or ""
        
        # Não carregar reservas aqui o que evita import circular
        self.__reservas = None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "documento": self.documento,
            "email": self.email,
            "telefone": self.telefone
        }

    @property
    def reservas(self):
        """
        Lazy loading de reservas: carrega somente quando acessar pela 1ª vez.
        """
        if self.__reservas is None:
            if self.id is None:
                self.__reservas = []
            else:
                # import local evita import circular
                from persistencia.reserva_dao import buscar_reservas_por_hospede
                self.__reservas = buscar_reservas_por_hospede(self.id)

        return self.__reservas

    def adicionar_reserva(self, reserva):
        """Adiciona reserva manualmente em memória."""
        if self.__reservas is None:
            self.__reservas = []
        self.__reservas.append(reserva)

    @staticmethod
    def from_db_row(row: sqlite3.Row):
        """Cria um objeto Hospede a partir de uma linha do banco de dados."""
        if not row:
            return None

        return Hospede(
            id=row["id"],
            nome=row["nome"],
            documento=row["documento"],
            email=row["email"],
            telefone=row["telefone"]
        )

