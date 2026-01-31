import math

def calculate_school(data: dict) -> dict:
    """
    Calculate raw materials for school notebooks
    """

    boxes = data["boxes"]
    size = data["size"]
    sheets = data["sheets"]
    gsm = data["gsm"]
    cover = data["cover"]

    SIZE_MAP = {
        "198X148": (198, 148),
        "A5": (148, 208),
        "B5": (172, 248),
        "A4": (208, 297),
    }

    sheets_per_large_sheet = {
        "198X148": 5,
        "A5": 4,
        "B5": 4,
        "A4": 3,
    }

    notebooks_per_cover = {
        "198X148": 10,
        "A5": 8,
        "B5": 8,
        "A4": 3,
    }

    large_sheet_dim = {
        "198X148": (305, 1000),
        "A5": (305, 840),
        "B5": (350, 1000),
        "A4": (425, 895),
    }

    BOX_RULES = [
    {"size": "198X148", "gsm": 55, "sheets": 40, "per_box": 160},
    {"size": "A5", "gsm": 55, "sheets": 40, "per_box": 160},
    {"size": "198X148", "gsm": 55, "sheets": 60, "per_box": 104},
    {"size": "198X148", "gsm": 55, "sheets": 64, "per_box": 96},
    {"size": "198X148", "gsm": 55, "sheets": 72, "per_box": 80},
    {"size": "198X148", "gsm": 55, "sheets": 96, "per_box": 64},
    ]

    # Notebook calculations
    def get_notebooks_from_box(size, sheets):
        for rule in BOX_RULES:
            if rule["size"] == size and rule["sheets"] == sheets:
                return rule["per_box"]
        raise ValueError("No matching rule found")

    number_of_notebooks = boxes * get_notebooks_from_box(size, sheets)

    # Raw paper calculation
    large_width_mm, large_height_mm = large_sheet_dim[size]
    large_sheet_quantity = number_of_notebooks * sheets / sheets_per_large_sheet[size] / 2
    total_paper_area = large_sheet_quantity * (large_width_mm / 1000) * (large_height_mm / 1000)
    total_raw_paper_weight_kg = total_paper_area * gsm / 1000

    # Actual paper calculation
    width_mm, height_mm = SIZE_MAP[size]
    area_m2 = (width_mm / 1000) * (height_mm / 1000)
    total_paper_weight_kg = (
        number_of_notebooks * sheets * area_m2 * gsm
    ) / 1000

    # Cover material estimation
    cover_quantity = number_of_notebooks / notebooks_per_cover[size]

    return {
        "product": f"school notebook {size} {sheets} sheets",
        "paper_weight_kg": round(total_paper_weight_kg, 2),
        "raw_paper_weight_kg": round(total_raw_paper_weight_kg, 2),
        "number_of_large_sheets_of_covers": math.ceil(cover_quantity),
    }
