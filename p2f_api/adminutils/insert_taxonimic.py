    
import pandas as pd
from p2f_api.service.keywords import create_dictionary_keyword


df_strat = pd.read_parquet("p2f_api/adminutils/strat_full_data.parquet")
df_gemet = pd.read_parquet("p2f_api/adminutils/gemet_full_data.parquet")

columns = ["keyword", "taxon", "taxonomic_id", "parent_keyword"]

for df in iter((df_strat, df_gemet)):
    for row in df[columns].itertuples(index=False):
        create_dictionary_keyword(
            keyword=row.keyword,
            taxon=row.taxon,
            taxonomic_id=row.taxonomic_id,
            parent_keyword=row.parent_keyword,
        )