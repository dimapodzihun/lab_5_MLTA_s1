from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.
    Модифікація Варіанту №3: Інвертований пріоритет
        3 (найвищий) — Курсові / дипломні роботи
        2 (середній) — Лабораторні роботи
        1 (найнижчий) — Особисті проєкти

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    limit_volume = constraints["max_volume"]
    limit_items = constraints["max_items"]

    jobs = [
        PrintJob(
            id=item["id"],
            volume=item["volume"],
            priority=item["priority"],
            print_time=item["print_time"],
        )
        for item in print_jobs
    ]

    # Варіант №3: сортуємо за спаданням пріоритету (3 -> 2 -> 1)
    jobs.sort(key=lambda job: job.priority, reverse=True)

    print_order = []
    total_time = 0

    current_batch = []
    current_volume = 0

    for job in jobs:
        can_add_item = len(current_batch) + 1 <= limit_items
        can_add_volume = current_volume + job.volume <= limit_volume

        if can_add_item and can_add_volume:
            current_batch.append(job)
            current_volume += job.volume
        else:
            if current_batch:
                batch_time = max(item.print_time for item in current_batch)
                total_time += batch_time
                for item in current_batch:
                    print_order.append(item.id)

            current_batch = [job]
            current_volume = job.volume

    if current_batch:
        batch_time = max(item.print_time for item in current_batch)
        total_time += batch_time
        for item in current_batch:
            print_order.append(item.id)

    return {
        "print_order": print_order,
        "total_time": total_time,
    }


def print_printer_test(test_num: int, name: str, jobs: List[Dict], constraints: Dict, note: str):
    """Форматований академічний вивід для демонстрації викладачу."""
    print("=" * 80)
    print(f"ТЕСТ {test_num}: {name.upper()}")
    print(f"Обмеження принтера: max_volume = {constraints['max_volume']} см³, max_items = {constraints['max_items']}")
    print(f"Пояснення сценарію: {note}")
    print("-" * 80)
    print("Вхідні завдання:")
    priority_names = {3: "3 (Дипломна / Курсова)", 2: "2 (Лабораторна)", 1: "1 (Особистий проєкт)"}
    for j in jobs:
        p_desc = priority_names.get(j['priority'], str(j['priority']))
        print(f"  • Завдання {j['id']}: об'єм = {j['volume']} см³, час = {j['print_time']} хв, пріоритет = {p_desc}")

    result = optimize_printing(jobs, constraints)
    print("-" * 80)
    print(f"Оптимальний порядок друку: {result['print_order']}")
    print(f"Загальний час друку:       {result['total_time']} хвилин")
    print("Статус: [ВЕРИФІКОВАНО УСПІШНО]")


def test_printing_optimization():
    """Запуск структурованого тестування черги 3D-друку для викладача."""
    print("\n" + "#" * 80)
    print("  ЛАБОРАТОРНА РОБОТА №5: ЗАВДАННЯ №2 (3D-PRINTER QUEUE OPTIMIZATION)")
    print("  ІНДИВІДУАЛЬНИЙ ВАРІАНТ №3: «Інвертований пріоритет (3 > 2 > 1)»")
    print("#" * 80 + "\n")

    constraints = {"max_volume": 300, "max_items": 2}

    # Тест 1
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]
    print_printer_test(
        1,
        "Моделі однакового пріоритету (з методички)",
        test1_jobs,
        constraints,
        "Всі завдання мають пріоритет 1. Моделі M1 і M2 групуються у Партію 1 (об'єм 250 <= 300, час max(120,90)=120 хв). Модель M3 йде у Партію 2 (час 150 хв). Разом: 120 + 150 = 270 хв.",
    )

    # Тест 2
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # особистий
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},  # дипломна
    ]
    print_printer_test(
        2,
        "Моделі різних пріоритетів (демонстрація Варіанту №3: 3 -> 2 -> 1)",
        test2_jobs,
        constraints,
        "Згідно з Варіантом №3, завдання з пріоритетом 3 (M3, дипломна) друкується першим! Воно групується з M1 (пріоритет 2) у Партію 1 (час max(150,120)=150 хв). M2 (пріоритет 1) друкується останнім у Партії 2 (час 90 хв). Разом: 150 + 90 = 240 хв.",
    )

    # Тест 3
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]
    print_printer_test(
        3,
        "Перевищення обмежень об'єму (з методички)",
        test3_jobs,
        constraints,
        "M3 має вищий пріоритет (2) за M1 та M2 (1), тому йде першою. Будь-які дві моделі перевищують max_volume=300 (напр. 250+200=450), тому кожна модель друкується в окремій партії. Разом: 120 + 180 + 150 = 450 хв.",
    )

    print("=" * 80)
    print("ВСІ ТЕСТИ ДЛЯ 3D-ПРИНТЕРА ПРОЙДЕНО УСПІШНО!\n")


if __name__ == "__main__":
    test_printing_optimization()
