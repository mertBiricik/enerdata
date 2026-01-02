#!/usr/bin/env python3
"""
Validate file 1 primary energy dataset by checking category sums and balance identities.
Reads from Excel via excel_to_js_data to ensure source-of-truth.
"""

from typing import Dict, Any, List, Tuple
from excel_to_html_converter import excel_to_js_data
import math

EXCEL = '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.xlsx'
TOL = 1e-6  # numeric tolerance in Mtep

def unbox(v: Any) -> float:
    if v is None:
        return None  # keep None
    if isinstance(v, dict) and 'value' in v:
        v = v['value']
    try:
        return float(v)
    except Exception:
        return None

def to_map(rows: List[Dict[str, Any]]) -> Dict[str, Dict[int, float]]:
    out: Dict[str, Dict[int, float]] = {}
    for r in rows:
        cat = r.get('Kategori')
        if not cat:
            continue
        year_map: Dict[int, float] = {}
        for k, v in r.items():
            if k == 'Kategori':
                continue
            try:
                y = int(k)
            except Exception:
                continue
            year_map[y] = unbox(v)
        out[cat] = year_map
    return out

def sum_cats(data: Dict[str, Dict[int, float]], cats: List[str], year: int) -> float:
    total = 0.0
    have = False
    for c in cats:
        v = data.get(c, {}).get(year)
        if v is None:
            continue
        total += v
        have = True
    return total if have else None

def compare(expected: float, actual: float) -> Tuple[bool, float]:
    if expected is None or actual is None:
        return True, 0.0  # skip if missing
    diff = actual - expected
    return abs(diff) <= TOL, diff

def main():
    rows = excel_to_js_data(EXCEL)
    data = to_map(rows)
    years = sorted({y for m in data.values() for y in m.keys()})

    checks = []

    # 1) Enerji arzı total identity
    supply_terms = ['Yerli Üretim (+)', 'İthalat (+)', 'Stok Değişimi (+/-)']
    supply_neg = ['İhracat (-)', 'İhrakiye (-)']
    supply_total = 'ENERJİ ÜRÜNLERİ ARZI'
    for y in years:
        positive = sum_cats(data, supply_terms, y)
        negative = sum_cats(data, supply_neg, y)
        expected = None if positive is None and negative is None else (positive or 0.0) - (negative or 0.0)
        actual = data.get(supply_total, {}).get(y)
        ok, diff = compare(expected, actual)
        checks.append(('Supply identity', y, expected, actual, diff, ok))

    # 2) Çevrim ve enerji sektörü = sum of its components
    trans_comps = ['Elektrik ve Isı Üretimi', 'İkincil Kömür Üreten/Tüketen Tesisler', 'Petrol Rafinerileri', 'İç Tüketim ve Kayıp']
    trans_total = 'ÇEVRİM VE ENERJİ SEKTÖRÜ'
    for y in years:
        expected = sum_cats(data, trans_comps, y)
        actual = data.get(trans_total, {}).get(y)
        ok, diff = compare(expected, actual)
        checks.append(('Transformation sum', y, expected, actual, diff, ok))

    # 3) Sanayi tüketimi = sum of industry subsectors
    ind_comps = ['Gıda', 'Şeker', 'Tekstil', 'Kağıt', 'Kimya-Petrokimya', 'Gübre',
                 'Cam ve Cam Ürünleri', 'Seramik', 'Çimento',
                 'Demir-Çelik', 'Demir Dışı Metaller',
                 'Motorlu Kara Taşıtları Sanayi', 'Diğer Sanayi']
    ind_total = 'SANAYİ TÜKETİMİ'
    for y in years:
        expected = sum_cats(data, ind_comps, y)
        actual = data.get(ind_total, {}).get(y)
        ok, diff = compare(expected, actual)
        checks.append(('Industry sum', y, expected, actual, diff, ok))

    # 4) Ulaştırma = sum of its subsectors
    transpt_comps = ['Demiryolları', 'Kara Yolları', 'İç Suyolları', 'Boru Hatları', 'Hava Yolları']
    transpt_total = 'ULAŞTIRMA'
    for y in years:
        expected = sum_cats(data, transpt_comps, y)
        actual = data.get(transpt_total, {}).get(y)
        ok, diff = compare(expected, actual)
        checks.append(('Transport sum', y, expected, actual, diff, ok))

    # 5) Sektörler toplamı = sum of all sector consumers
    sectors_total = 'SEKTÖRLER TOPLAMI'
    sector_consumers = [
        ind_total, transpt_total,
        'Konut, Ticarethane ve Hizmetler',
        'Tarım ve Hayvancılık',
        'Diğer Sektörler'
    ]
    for y in years:
        expected = sum_cats(data, sector_consumers, y)
        actual = data.get(sectors_total, {}).get(y)
        ok, diff = compare(expected, actual)
        checks.append(('Sectors sum', y, expected, actual, diff, ok))

    # 6) Global balance: Supply + Transformation ≈ Sectors + Statistical Difference
    stat_diff = 'İstatistiksel Fark (+/-)'
    for y in years:
        supp = data.get(supply_total, {}).get(y)
        trans_val = data.get(trans_total, {}).get(y)
        sectors = data.get(sectors_total, {}).get(y)
        stat = data.get(stat_diff, {}).get(y)
        expected = None if supp is None and trans_val is None else (supp or 0.0) + (trans_val or 0.0)
        actual = None if sectors is None and stat is None else (sectors or 0.0) + (stat or 0.0)
        ok, diff = compare(expected, actual)
        checks.append(('Global balance', y, expected, actual, diff, ok))

    failed = [c for c in checks if not c[5]]
    print(f"Total checks: {len(checks)}, OK: {len(checks)-len(failed)}, FAIL: {len(failed)}")
    def fmt(v):
        return 'None' if v is None else f"{v:.6f}"
    for name, y, exp, act, diff, ok in failed[:50]:
        print(f"[{name}] {y}: expected {fmt(exp)} vs actual {fmt(act)} diff {fmt(diff)}")

if __name__ == '__main__':
    main()

