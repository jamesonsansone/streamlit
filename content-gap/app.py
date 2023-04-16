if st.button("Compare Rankings"):
    featured_df = process_csv(featured_file, 'Featured Domain')
    comp_dfs = [process_csv(comp_file, f'Competitor {i + 1}') for i, comp_file in enumerate(comp_files) if comp_file is not None]

    if featured_df is not None and len(comp_dfs) > 0:
        all_dfs = [featured_df] + comp_dfs
        combined_df = pd.concat(all_dfs, axis=0)
        combined_df = combined_df.groupby(['Keyword', 'Volume', 'Domain']).agg(Avg_Current_Position=('Featured Domain', 'mean')).reset_index()
        pivot_df = combined_df.pivot_table(index=['Keyword', 'Volume'], columns='Domain', values='Avg_Current_Position').reset_index()

        domain_columns = [df['Domain'].iloc[0] for df in all_dfs]
        
        print("domain_columns:", domain_columns)
        print("pivot_df columns:", pivot_df.columns)

        pivot_df.columns = ['Keyword', 'Volume'] + domain_columns

        pivot_df['# of Ranking Domains'] = pivot_df.iloc[:, 2:].apply(lambda x: (x <= 20).sum(), axis=1)
        pivot_df['Featured Highest'] = pivot_df.apply(lambda x: x[2] == min(x[2:len(domain_columns) + 2]), axis=1)

        st.write(pivot_df)

        if st.button("Export to CSV"):
            pivot_df.to_csv("keyword_rankings_comparison.csv", index=False)
            st.markdown("[Download CSV](keyword_rankings_comparison.csv)")

        not_highest_df = pivot_df[pivot_df['Featured Highest'] == False].sort_values(by='Volume', ascending=False)
        st.subheader("Featured Domain not Highest")
        st.write(not_highest_df)

    else:
        st.write("Please upload the required CSV files.")
