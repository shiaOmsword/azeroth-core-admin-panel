def format_money(money: int) -> str:
    gold, remainder = divmod(money, 10_000)
    silver, copper = divmod(remainder, 100)
    return f"{gold}g. {silver}s. {copper}c."