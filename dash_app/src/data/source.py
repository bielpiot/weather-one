from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import pandas as pd

from .loader import DataSchema


@dataclass
class DataSource:
    _data = pd.DataFrame

    def filter(self, locations: Optional[List[str]], measures: Optional[List[str]]) -> DataSource:
        if locations is None:
            locations = self.locations_list
        if measures is None:
            measures = self.measures_list
        filtered_data = self._data.query('location in @locations')
        filtered_data = filtered_data.loc[measures]
        return DataSource(filtered_data)

    @property
    def locations_list(self) -> List[str]:
        return sorted(set(self._data[DataSchema.location].to_list()))
    
    @property
    def measures_list(self) -> List[str]:
        return [col for col in list(self._data.columns()) if col not in (DataSchema.location, DataSchema.timepoint)]
    
    @property
    def row_count(self) -> int:
        return self._data.shape[0]
    
    @property
    def secondary_measures_list(self) -> List[str]:
        return [msr for msr in self.measures_list if msr in (DataSchema.cloudcover, DataSchema.lifted_index,
                                                              DataSchema.tranparency, DataSchema.rh2m,
                                                              DataSchema.wind10m_speed)]