import json
from pathlib import Path
from datetime import datetime, date

ROOT = Path(__file__).parents[1]  # pasta do projeto
DEFAULT_SETTINGS = {
    "checkin_hora": "14:00",
    "checkout_hora": "12:00",
    "tolerancia_checkin_minutos": 120,
    "tolerancia_checkout_minutos": 60,
    "noshow_tolerancia_minutos": 180,
    "multa_cancelamento_percentual": 0.5,
    "multiplicador_fim_de_semana": 1.2,
    "temporadas": []
}

class ConfigService:
    def __init__(self, path: Path = None):
        self.path = Path(path) if path else ROOT / "settings.json"
        self._data = {}
        self.reload()

    def reload(self):
        if not self.path.exists():
            self._data = DEFAULT_SETTINGS.copy()
            return
        with open(self.path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def get(self, key, default=None):
        return self._data.get(key, DEFAULT_SETTINGS.get(key, default))

    def temporadas(self):
        """
        Retorna lista de temporadas como dicionários com campos:
        - nome
        - inicio: date
        - fim: date
        - multiplicador: float
        """
        temp = []
        for t in self._data.get("temporadas", []):
            inicio = datetime.fromisoformat(t["inicio"]).date() if isinstance(t["inicio"], str) else t["inicio"]
            fim = datetime.fromisoformat(t["fim"]).date() if isinstance(t["fim"], str) else t["fim"]
            temp.append({
                "nome": t.get("nome"),
                "inicio": inicio,
                "fim": fim,
                "multiplicador": float(t.get("multiplicador", 1.0))
            })
        return temp

    def multiplicador_fim_de_semana(self):
        return float(self.get("multiplicador_fim_de_semana", 1.0))

    def multa_cancelamento_percentual(self):
        return float(self.get("multa_cancelamento_percentual", 0.5))

    def noshow_tolerancia_minutos(self):
        return int(self.get("noshow_tolerancia_minutos", 180))

    def checkin_hora(self):
        return self.get("checkin_hora", "14:00")

    def checkout_hora(self):
        return self.get("checkout_hora", "12:00")

# Instância global (padrão) que outros módulos podem importar
config_service = ConfigService()
