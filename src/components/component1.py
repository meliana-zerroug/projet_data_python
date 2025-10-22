import pandas as pd
import plotly.express as px
import plotly.io as pio

# Lire les données
df = pd.read_csv("rawdata.csv", dtype=str)

# --- Préparation des données PIB (par zone) ---
mask_pib = df['Produit'].str.contains('PIB', case=False, na=False) & (df['Élément'] == 'Valeur')
df_pib = df[mask_pib].copy()
df_pib['Année_num'] = pd.to_numeric(df_pib['Année'], errors='coerce')
df_pib['Valeur_PIB'] = pd.to_numeric(df_pib['Valeur'].str.replace(',', ''), errors='coerce')
df_pib = df_pib.dropna(subset=['Valeur_PIB'])

if df_pib.empty:
	print('Aucune donnée PIB trouvée dans rawdata.csv (filtre Produit contenant "PIB").')
else:
	# Pour chaque zone, garder la valeur 2023 si présente, sinon la plus récente
	def pick_idx_year(series):
		if 2023 in series.values:
			return series[series == 2023].index[0]
		return series.idxmax()

	idx_pib = df_pib.groupby('Zone')['Année_num'].apply(pick_idx_year)
	df_pib_latest = df_pib.loc[idx_pib].copy()
	df_pib_latest = df_pib_latest.sort_values('Valeur_PIB', ascending=False)

	# Figure 1 : PIB par zone (dernier an disponible / 2023 preferred)
	fig_pib = px.bar(df_pib_latest, x='Zone', y='Valeur_PIB',
					 title='PIB par habitant (valeur) par zone - 2023 (ou dernière année disponible)',
					 labels={'Valeur_PIB':'PIB (Int$/cap)', 'Zone':'Zone'})
	fig_pib.update_layout(xaxis={'categoryorder':'total descending'}, height=600)

	# --- Préparation des données pour les personnes sous-alimentées et obèses ---
	# Filtrer sous-alimentation et obésité (élément = Valeur)
	mask_under = df['Produit'].str.contains('sous-aliment', case=False, na=False) & (df['Élément'] == 'Valeur')
	mask_obese = df['Produit'].str.contains('obés|obes', case=False, na=False) & (df['Élément'] == 'Valeur')

	df_under = df[mask_under].copy()
	df_obese = df[mask_obese].copy()

	# Convertir
	for d in (df_under, df_obese):
		d['Année_num'] = pd.to_numeric(d['Année'], errors='coerce')
		d['Valeur_num'] = pd.to_numeric(d['Valeur'].str.replace(',', ''), errors='coerce')

	# Fonction utilitaire pour choisir la valeur 2023 si présente sinon la plus récente
	def pick_latest_values(dframe):
		dframe = dframe.dropna(subset=['Valeur_num'])
		if dframe.empty:
			return pd.DataFrame(columns=['Zone', 'Valeur_num'])
		idx = dframe.groupby('Zone')['Année_num'].apply(pick_idx_year)
		return dframe.loc[idx, ['Zone', 'Valeur_num']].set_index('Zone')

	under_latest = pick_latest_values(df_under)
	obese_latest = pick_latest_values(df_obese)

	# Combiner par Zone : sum des deux (les valeurs sont en millions selon le fichier)
	combined = pd.DataFrame(index=df_pib_latest['Zone'])
	combined = combined[~combined.index.duplicated()]
	combined.index.name = 'Zone'
	combined = combined.join(under_latest.rename(columns={'Valeur_num':'Under_millions'}), how='left')
	combined = combined.join(obese_latest.rename(columns={'Valeur_num':'Obese_millions'}), how='left')
	combined['Under_millions'] = combined['Under_millions'].fillna(0)
	combined['Obese_millions'] = combined['Obese_millions'].fillna(0)
	combined['Sum_millions'] = combined['Under_millions'] + combined['Obese_millions']

	# Joindre le PIB correspondant (Valeur_PIB) — index de df_pib_latest est pas Zone index, donc aligner
	pib_map = df_pib_latest.set_index('Zone')['Valeur_PIB']
	combined = combined.join(pib_map.rename('Valeur_PIB'), how='left')

	# Nettoyer lignes sans PIB
	combined = combined.dropna(subset=['Valeur_PIB'])

	if combined.empty:
		print('Aucune correspondance PIB <-> population trouvée pour construire l\'histogramme.')
	else:
		# Créer un histogramme : somme des personnes (sous-alim + obésité) agrégée par bins de PIB
		# Valeur_PIB est le PIB par habitant (Int$/cap), Sum_millions en millions
		fig_hist = px.histogram(combined.reset_index(), x='Valeur_PIB', y='Sum_millions',
								histfunc='sum', nbins=20,
								title='Somme personnes sous-alimentées + obèses (millions) agrégées par bins de PIB par habitant',
								labels={'Valeur_PIB':'PIB par habitant (Int$/cap)', 'Sum_millions':'Somme (millions de personnes)'} )
		fig_hist.update_layout(height=500)

		# Exporter les deux figures dans un seul fichier HTML (fig_pib d'abord, puis fig_hist)
		html1 = pio.to_html(fig_pib, full_html=False, include_plotlyjs='cdn')
		html2 = pio.to_html(fig_hist, full_html=False, include_plotlyjs=False)
		out_file = 'pib_and_people.html'
		with open(out_file, 'w', encoding='utf-8') as f:
			f.write('<html><head><meta charset="utf-8"></head><body>\n')
			f.write(html1)
			f.write('<hr style="margin:40px 0;">\n')
			f.write(html2)
			f.write('\n</body></html>')

		print(f"Saved {out_file} with {len(df_pib_latest)} zones and histogram aggregated over {len(combined)} zones.")