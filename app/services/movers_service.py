from app.services.price_service import daily_change



def get_changes_for_symbols(symbols: list[str]) -> list[dict]:
    results = []
    for sym in symbols:
        data = daily_change(sym)
        if data is not None:
            results.append(data)
    return results

def sort_by_change(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: r["percent_change"], reverse=True)

def get_movers(rows: list[dict], top_n: int=5) -> dict:
    rows = sorted(rows, key=lambda r: r["percent_change"],reverse=True)


    return {
        "top": rows[:top_n],
        "bottom": rows[-top_n:][::-1],
        "count": len(rows)
    }

def compute_movers(symbols: list[str], top_n) -> list[dict]:
    results = get_changes_for_symbols(symbols)
    sorted_results = sort_by_change(results)
    return get_movers(sorted_results, top_n=top_n)


