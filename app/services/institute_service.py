import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import HTTPException

# Путь к директории с JSON файлами
DATA_DIR = Path(__file__).parent.parent / "data"


class InstituteService:
    """Сервис для работы с институтами и группами"""

    def __init__(self):
        self._institutes_cache: Optional[List[Dict]] = None
        self._groups_cache: Dict[str, List[Dict]] = {}
        self._load_all_institutes()

    def _load_all_institutes(self):
        """Загрузка всех институтов при инициализации"""
        if not DATA_DIR.exists():
            raise RuntimeError(f"Data directory not found: {DATA_DIR}")

        self._institutes_cache = []  # Инициализируем как список

        # Читаем все JSON файлы
        for json_file in DATA_DIR.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Проверяем структуру данных
                    if not isinstance(data, dict) or "id" not in data or "name" not in data:
                        print(f"Skipping {json_file}: invalid structure")
                        continue

                    # Добавляем институт в кэш
                    self._institutes_cache.append({
                        "id": data["id"],
                        "name": data["name"]
                    })

                    # Кэшируем группы
                    self._groups_cache[data["id"]] = data.get("groups", [])

            except json.JSONDecodeError as e:
                print(f"JSON decode error {json_file}: {e}")
                continue
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
                continue

        if not self._institutes_cache:
            raise RuntimeError("No institutes data found")

    def get_all_institutes(self) -> List[Dict[str, str]]:
        """
        Получить список всех институтов

        Returns:
            [{"id": "ims", "name": "Институт..."}, ...]
        """
        return self._institutes_cache

    def get_institute_groups(self, institute_id: str) -> List[Dict[str, str]]:
        """
        Получить список групп конкретного института

        Args:
            institute_id: ID института (например, "ims")

        Returns:
            [{"key": "370", "name": "И41 - Менеджмент"}, ...]

        Raises:
            HTTPException: Если институт не найден
        """
        if institute_id not in self._groups_cache:
            raise HTTPException(
                status_code=404,
                detail=f"Institute with id '{institute_id}' not found"
            )

        return self._groups_cache[institute_id]

    def validate_group_id(self, group_id: int) -> bool:
        """
        Проверить существование group_id

        Args:
            group_id: ID группы

        Returns:
            True если группа существует
        """
        group_id_str = str(group_id)

        for groups in self._groups_cache.values():
            if any(g["key"] == group_id_str for g in groups):
                return True

        return False

    def get_group_info(self, group_id: int) -> Optional[Dict]:
        """
        Получить информацию о группе по ID

        Args:
            group_id: ID группы

        Returns:
            {"key": "370", "name": "...", "institute_id": "ims"} или None
        """
        group_id_str = str(group_id)

        for institute_id, groups in self._groups_cache.items():
            for group in groups:
                if group["key"] == group_id_str:
                    return {
                        **group,
                        "institute_id": institute_id
                    }

        return None


# Singleton instance
_institute_service = None


def get_institute_service() -> InstituteService:
    """Получить singleton instance сервиса"""
    global _institute_service
    if _institute_service is None:
        _institute_service = InstituteService()
    return _institute_service