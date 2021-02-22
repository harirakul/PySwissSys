import dbf
import pandas as pd

def df2dbf(filename: str, df: pd.DataFrame, on_disk = False) -> dbf.Table:
    field_specs=' C(8); '.join(df.columns) + " C(8)"
    table = dbf.Table(
        filename = filename,
        field_specs=field_specs,
        on_disk=on_disk
    )
    table.open(mode=dbf.READ_WRITE)
    for idx, row in df.iterrows():
        table.append(tuple([str(i).strip() for i in row.tolist()]))
    
    return table

def tdexport(tnmt):
    df = pd.DataFrame()
    
    df["D_EVENT_ID"] = ""
    df["D_SEC_NUM"] = [1 for i in range(len(tnmt.players))]
    df["D_PAIR_NUM"] = [i + 1 for i in range(len(tnmt.players))]
    df["D_MEM_ID"] = tnmt.table["USCF ID"].tolist()
    df["D_NAME"] = tnmt.table["Name"].tolist()
    df["D_STATE"] = ""
    df["D_RATING"] = tnmt.table["Rating"].tolist()

    for i in range(1, tnmt.round):
        df[f"D_RND0{i}"] = tnmt.table[f"Rnd {i}"].tolist()

    df2dbf("tdexport", df, on_disk=True)
    return df

if __name__ == "__main__":
    import td
    t = td.Tournament.load(r"databases\tnmts\NewTest.tnmt")
    t.update_standings()
    print(tdexport(t))