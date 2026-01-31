import math

def calculate_spiral(data: dict) -> dict:
    """
    Calculate raw materials for spiral notebooks
    """

    number = data["number"]
    size = data["size"]
    sheets = data["sheets"]
    gsm = data["gsm"]

    # size dimensions (mm)
    SIZE_MAP = {
        "A5": (148, 209),
        "B5": (172, 248),
        "A4": (208, 297),
    }

    sheets_per_large_sheet = {
        "A5": 8,
        "B5": 8,
        "A4": 6,
    }

    large_sheet_dim = {
        "A5": (305, 840),
        "B5": (350, 1000),
        "A4": (425, 895),
    }

    BOX_RULES = [
    {"size": "A5", "gsm": 55, "sheets": 80, "per_box": 80},
    {"size": "A5", "gsm": 55, "sheets": 120, "per_box": 60},
    {"size": "A5", "gsm": 55, "sheets": 160, "per_box": 40},
    {"size": "A5", "gsm": 55, "sheets": 200, "per_box": 40},
    {"size": "B5", "gsm": 55, "sheets": 80, "per_box": 40},
    {"size": "B5", "gsm": 55, "sheets": 120, "per_box": 30},
    {"size": "B5", "gsm": 55, "sheets": 160, "per_box": 20},
    {"size": "B5", "gsm": 55, "sheets": 200, "per_box": 20},
    {"size": "A4", "gsm": 55, "sheets": 80, "per_box": 40},
    {"size": "A4", "gsm": 55, "sheets": 120, "per_box": 30},
    {"size": "A4", "gsm": 55, "sheets": 160, "per_box": 20},
    {"size": "A4", "gsm": 55, "sheets": 200, "per_box": 20},
]

    width_mm, height_mm = SIZE_MAP[size]

    # Actual paper weight calculation
    # sheets × notebooks × area × gsm
    area_m2 = (width_mm / 1000) * (height_mm / 1000)
    total_paper_weight_kg = (
        number * sheets * area_m2 * gsm
    ) / 1000

    # Raw paper weight calculation
    large_width_mm, large_height_mm = large_sheet_dim[size]
    large_sheet_quantity = number * sheets / sheets_per_large_sheet[size]
    total_paper_area = large_sheet_quantity * (large_width_mm / 1000) * (large_height_mm / 1000)
    total_raw_paper_weight_kg = total_paper_area * gsm / 1000

    # Cover calculations
    cover_quantity = number  / sheets_per_large_sheet[size]

    # Boxes calculations
    def get_notebooks_per_box(size, gsm, sheets):
        for rule in BOX_RULES:
            if rule["size"] == size and rule["gsm"] == gsm and rule["sheets"] == sheets:
                return rule["per_box"]
        raise ValueError("No matching rule found")

    number_of_boxes = number / get_notebooks_per_box(size, gsm, sheets)

    return {
        "product": f"Spiral Notebook {size} {sheets} sheets",
        "paper_weight_kg": round(total_paper_weight_kg, 2),
        "raw_paper_weight_kg": round(total_raw_paper_weight_kg, 2),
        "number_of_large_sheets_of_covers": math.ceil(cover_quantity),
        "number_of_boxes": math.ceil(number_of_boxes)
    }
