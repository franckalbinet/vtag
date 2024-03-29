# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['src', 'df_all', 'timestamp_to_seconds', 'csv_to_m3u', 'get_all_tags']

# %% ../nbs/00_core.ipynb 5
def timestamp_to_seconds(timestamp):
    # Split the timestamp into hours, minutes, and seconds
    hours, minutes, seconds = map(int, timestamp.split(':'))

    # Convert the timestamp to seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds

# %% ../nbs/00_core.ipynb 8
def csv_to_m3u(src, dest_dir='../_data/asac'):
    dest = Path(src).stem
    df = pd.read_csv(src)
    df.time = df.time.apply(timestamp_to_seconds)
    bookmarks = ', '.join(df[['time', 'name']].apply(lambda row: f"{{name={row['name']},time={row['time']}}}", axis=1).tolist())
    extm3u = '#EXTM3U'
    extvlcopt = f'#EXTVLCOPT:bookmarks={bookmarks}'
    fname = f'{dest}.mp4'
    result_string = f'{extm3u}\n{extvlcopt}\n{fname}'
    file_path = Path(dest_dir) / f'{dest}.m3u'
    with open(file_path, "w") as file:
        file.write(result_string)

# src = '../_data/asac/8-session-2-previous-year.csv'
src = '../_data/asac/12-session.csv'
csv_to_m3u(src)

# %% ../nbs/00_core.ipynb 11
def get_all_tags(src_dir):
    fnames = [p for p in Path(src_dir).ls() if p.suffix == '.csv']
    data = []
    for fname in fnames:
        df = pd.read_csv(fname) 
        df['fname'] = fname.stem
        df['n_lesson'] = df['fname'].apply(lambda row: int(re.search(r'(\d+)-', row).group(1)))
        data.append(df)
    df_all = pd.concat(data)
    return df_all.sort_values(by=['n_lesson', 'time'], ascending=True)
    
df_all = get_all_tags('../_data/asac'); df_all
