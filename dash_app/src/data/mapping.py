from typing import Dict, Any


CLOUDCOVER_DESC_TABLE = {
                             1: '0%-6%', 2: '6%-19%', 3: '19%-31%', 4: '31%-44%',
                             5: '44%-56%', 6: '56%-69%', 7: '69%-81%', 8: '81%-94%',
                             9: '94%-100%'
                             }
    
LIFTED_INDEX_DESC_TABLE = {
                            1: 'Below -7', 2: '-7 to -5', 3: '-5 to -3',
                            4: '-3 to 0', 5: '0 to 4', 6: '4 to 8',
                            7: '8 to 11', 8: 'Over 11'
                            }

LIFTED_INDEX_SCALED_TABLE = {
                             -10: 1, -6: 2, -4: 3, -1: 4, 2: 5, 6: 6, 10: 7, 15: 8
                            }


TRANSPARENCY_DESC_TABLE = {
                            1: '<0.3', 2: '0.3-0.4', 3: '0.4-0.5',
                            4: '0.5-0.6', 5: '0.6-0.7', 6: '0.7-0.85',
                            7: '0.85-1', 8: '>1'
                            }

RH2M_DESC_TABLE_START = {**{n: f'{((n+4)*5)}%-{(n+5)*5}%' for n in range(-4,16)},
                    **{16: '100%'}}

RH2M_SCALED_TABLE = {
                     k-6 : k/2 for k in range(2, 23)
                    }

RH2M_DESC_TABLE_FINAL = {RH2M_SCALED_TABLE.get(k, k) : v for k, v in RH2M_DESC_TABLE_START.items()}

WIND_SPEEC_DESC_TABLE = {
                    1: 'Below 0.3m/s (calm)', 2: '0.3-3.4m/s (light)',
                    3: '3.4-8.0m/s (moderate)', 4: '8.0-10.8m/s (fresh)',
                    5: '10.8-17.2m/s (strong)', 6: '17.2-24.5m/s (gale)',
                    7: '24.5-32.6m/s (storm)', 8: 'Over 32.6m/s (hurricane)'
                    }

print(RH2M_DESC_TABLE_FINAL)
print(LIFTED_INDEX_DESC_TABLE)
