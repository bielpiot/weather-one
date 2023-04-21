from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import pandas as pd

from .loader import DataSchema


@dataclass
class DataSource:
    data : pd.DataFrame

    def filter(self, location: str, measures: Optional[List[str]]) -> DataSource:
        if measures is None:
            measures = self.graphed_measures_list
        descs = [col for col in self.data.columns if col.endswith('_desc')]
        static_cols = ['location', 'timepoint', 'wind10m_direction', 'prec_type']
        filtereddata = self.data[self.data.location == location]
        filtereddata = filtereddata[[*static_cols, *descs, *measures]]
        filtereddata.sort_values(by='timepoint', inplace=True)
        return DataSource(filtereddata)

    @property
    def locations_list(self) -> List[str]:
        return sorted(self.data.location.unique())
    
    @property
    def measures_list(self) -> List[str]:
        return [col for col in list(self.data.columns) if col not in ('location', 'timepoint')]
    
    @property
    def graphed_measures_list(self) -> List[str]:
        return list(set(self.measures_list).intersection({'cloudcover', 'lifted_index', 'seeing', 'transparency',
                                                              'rh2m', 'wind10m_speed', 'temp2m'}))
    
    @property
    def row_count(self) -> int:
        return self.data.shape[0]
    
    @property
    def secondary_measures_list(self) -> List[str]:
        return list(set(self.measures_list).intersection({'cloudcover', 'lifted_index', 'seeing', 'transparency',
                                                              'rh2m', 'wind10m_speed'}))
        # return [msr for msr in self.measures_list if msr in ('cloudcover', 'lifted_index', 'transparency',
        #                                                       'rh2m', 'wind10m_speed')]
    
    @property
    def descriptive_measures_list(self) -> List[str]:
        return list(set(self.measures_list).intersection({'prec_type', 'wind10m_direction'}))
    
    def build_data_table(self, sort_by: str = 'timepoint') -> pd.DataFrame:
        """
        All operations to get desirable final data form
        1. sort
        2. open for extension - when need for additional operations arises split into separate functions
        """
        return self.data.sort_values(by=[sort_by])