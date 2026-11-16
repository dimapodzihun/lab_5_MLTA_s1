from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію (Top-Down).
    Модифікація Варіанту №3: Премія за цілий стрижень (+5 грошових одиниць).

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком частин та кількістю розрізів
    """
    memo = {}

    def get_best_cuts(n: int):
        """Рекурсивний пошук оптимального розрізання для довжини n без бонусу."""
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = -1
        best_cuts = []
        for i in range(1, n + 1):
            sub_profit, sub_cuts = get_best_cuts(n - i)
            total = prices[i - 1] + sub_profit
            if total > max_profit:
                max_profit = total
                best_cuts = [i] + sub_cuts

        memo[n] = (max_profit, best_cuts)
        return memo[n]

    # Варіант А: Стрижень залишається цілим (діє бонус +5)
    whole_profit = prices[length - 1] + 5
    whole_cuts = [length]

    # Варіант Б: Стрижень розрізається принаймні один раз (бонус не діє)
    best_cut_profit = -1
    best_cut_pieces = []
    for i in range(1, length):
        sub_profit, sub_cuts = get_best_cuts(length - i)
        total = prices[i - 1] + sub_profit
        if total > best_cut_profit:
            best_cut_profit = total
            best_cut_pieces = [i] + sub_cuts

    # Явне порівняння згідно з критерієм прийняття Варіанту №3
    if length == 1 or whole_profit >= best_cut_profit:
        max_profit = whole_profit
        cuts = whole_cuts
    else:
        max_profit = best_cut_profit
        cuts = best_cut_pieces

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1,
        "_whole_profit": whole_profit,
        "_cut_profit": best_cut_profit if best_cut_profit != -1 else 0,
        "_cut_pieces": best_cut_pieces,
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію (Bottom-Up).
    Модифікація Варіанту №3: Премія за цілий стрижень (+5 грошових одиниць).

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком частин та кількістю розрізів
    """
    dp = [0] * (length + 1)
    cuts_history = [[] for _ in range(length + 1)]

    # Заповнення таблиці ДП для всіх менших довжин (підзадачі без бонусу)
    for current_len in range(1, length):
        max_profit = -1
        best_cuts = []
        for i in range(1, current_len + 1):
            total = prices[i - 1] + dp[current_len - i]
            if total > max_profit:
                max_profit = total
                best_cuts = cuts_history[current_len - i] + [i]
        dp[current_len] = max_profit
        cuts_history[current_len] = best_cuts

    # Варіант А: Стрижень залишається цілим (діє бонус +5)
    whole_profit = prices[length - 1] + 5
    whole_cuts = [length]

    # Варіант Б: Стрижень розрізається принаймні один раз (бонус не діє)
    best_cut_profit = -1
    best_cut_pieces = []
    for i in range(1, length):
        total = prices[i - 1] + dp[length - i]
        if total > best_cut_profit:
            best_cut_profit = total
            best_cut_pieces = cuts_history[length - i] + [i]

    # Явне порівняння згідно з критерієм прийняття Варіанту №3
    if length == 1 or whole_profit >= best_cut_profit:
        max_profit = whole_profit
        cuts = whole_cuts
    else:
        max_profit = best_cut_profit
        cuts = best_cut_pieces

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1,
        "_whole_profit": whole_profit,
        "_cut_profit": best_cut_profit if best_cut_profit != -1 else 0,
        "_cut_pieces": best_cut_pieces,
    }


def print_test_case(test_num: int, name: str, length: int, prices: List[int], note: str):
    """Форматований академічний вивід для демонстрації викладачу."""
    memo_res = rod_cutting_memo(length, prices)
    table_res = rod_cutting_table(length, prices)

    whole = memo_res["_whole_profit"]
    cut_val = memo_res["_cut_profit"]
    cut_pieces = memo_res["_cut_pieces"]

    print("=" * 80)
    print(f"ТЕСТ {test_num}: {name.upper()}")
    print(f"Вхідні дані: довжина стрижня N = {length}, масив цін = {prices}")
    print(f"Аналітичний коментар: {note}")
    print("-" * 80)
    print("ЯВНЕ ПОРІВНЯННЯ ВАРІАНТІВ (згідно з критерієм прийняття Варіанту №3):")
    print(f"  • Стратегія 1 (БЕЗ розрізів): ціна {prices[length - 1]} + бонус 5 = {whole} грн")
    if length > 1:
        print(f"  • Стратегія 2 (З розрізами):  найкращий розпил {cut_pieces} = {cut_val} грн (без бонусу)")
    else:
        print("  • Стратегія 2 (З розрізами):  довжину 1 розрізати неможливо")

    if whole >= cut_val:
        reason = f"Стратегія 1 вигідніша ({whole} >= {cut_val}) -> стрижень залишається цілим (0 розрізів)."
    else:
        reason = f"Стратегія 2 вигідніша ({cut_val} > {whole}) -> вигідніше розрізати навіть без бонусу!"
    print(f"  => ВИСНОВОК АЛГОРИТМУ: {reason}")
    print("-" * 80)
    print(f"Результат мемоізації: max_profit = {memo_res['max_profit']}, cuts = {memo_res['cuts']}, розрізів = {memo_res['number_of_cuts']}")
    print(f"Результат табуляції:  max_profit = {table_res['max_profit']}, cuts = {table_res['cuts']}, розрізів = {table_res['number_of_cuts']}")
    assert memo_res["max_profit"] == table_res["max_profit"], "Помилка розбіжності результатів!"
    print("Статус: [ВЕРИФІКОВАНО УСПІШНО]")


def run_tests():
    """Запуск структурованого набору тестів для викладача."""
    print("\n" + "#" * 80)
    print("  ЛАБОРАТОРНА РОБОТА №5: ЗАВДАННЯ №1 (ROD CUTTING PROBLEM)")
    print("  ІНДИВІДУАЛЬНИЙ ВАРІАНТ №3: «Премія за цілий стрижень (+5 грошових одиниць)»")
    print("#" * 80 + "\n")

    # ЧАСТИНА 1: Обов'язкові тести з методичних вказівок
    print(">>> ЧАСТИНА 1: БАЗОВІ ТЕСТИ З МЕТОДИЧКИ (з урахуванням модифікації Варіанту №3)")

    print_test_case(
        1,
        "Базовий випадок (з методички)",
        5,
        [2, 5, 7, 8, 10],
        "У базовій задачі без бонусу оптимально різати на [2, 2, 1] за 12 грн. Проте бонус +5 робить цілий стрижень вигіднішим: 10 + 5 = 15 грн.",
    )

    print_test_case(
        2,
        "Оптимально не різати (з методички)",
        3,
        [1, 3, 8],
        "Цілий стрижень переважає розпил навіть без бонусу (8 > 4). З бонусом +5 прибуток зростає до 13 грн.",
    )

    print_test_case(
        3,
        "Рівномірні розрізи (з методички)",
        4,
        [3, 5, 6, 7],
        "Без бонусу вигідно різати на 4 частини по 1 (3*4 = 12 грн). З бонусом цілий стрижень дає рівно ті самі 7 + 5 = 12 грн. Обирається варіант без розрізів (0 трудовитрат).",
    )

    # ЧАСТИНА 2: Дослідницькі тести для демонстрації всіх можливостей
    print("\n>>> ЧАСТИНА 2: ДОСЛІДНИЦЬКІ ТЕСТИ (демонстрація випадків, коли розрізати вигідніше за бонус)")

    print_test_case(
        4,
        "Розрізання вигідніше за бонус (дорогі дрібні частини)",
        5,
        [5, 8, 9, 10, 11],
        "Ціна 1 метра настільки висока (5 грн), що розрізати на [1, 1, 1, 1, 1] дає 25 грн. Це значно перевищує цілий стрижень з бонусом (11 + 5 = 16 грн). Алгоритм обирає розрізи!",
    )

    print_test_case(
        5,
        "Комбінований розпил [2, 3] перемагає бонус",
        5,
        [2, 7, 10, 10, 11],
        "Розпил на 2 м (7 грн) і 3 м (10 грн) дає 17 грн, що більше за цілий стрижень з бонусом (11 + 5 = 16 грн). Обирається розріз на 2 частини.",
    )

    print_test_case(
        6,
        "Граничний випадок (довжина N = 1)",
        1,
        [4],
        "Стрижень одиничної довжини розрізати неможливо. Він завжди продається цілим: 4 + 5 = 9 грн.",
    )

    print("=" * 80)
    print("ВСІ ТЕСТОВІ СЦЕНАРІЇ ПРОЙДЕНО УСПІШНО!\n")


if __name__ == "__main__":
    run_tests()
