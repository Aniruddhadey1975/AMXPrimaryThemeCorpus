def Input_from_User_Primary_Theme_rev3():
    merged_articles = pd.read_csv('mergedArticles.csv')

    
    # Sample data for demonstration
    # Sample data for demonstration
    data = {
    'Corporate': ["Social Responsibility", "Openings & Closure", "CXO Mention / Movement", "Events", "Profit", "Bootleg / Copies", "Launch"],
    'Sensitive_Skin_Massaging': ["blemish, blemishes", "breakout(s)", "fragrance free", "unscented", "gentle", "hypoallergenic", "irritating, irritated", "noncomedogenic", "oil-free", "redness", "sensitive sensitivity", "vulnerable", "distressed", "delicate", "reactive reaction", "compromised", "exposed", "damage", "itch", "dry", "rash", "eczema", "psoriasis", "acne", "rosacea", "dermatitis", "oncology", "cancer", "healthy", "hydrating hydrate hydration", "microbiome", "moisturizing, moisturize, moisturization", "prebiotic", "strengthen", "protect", "improves", "wash", "soft", "firm", "cracked", "fragile", "paraben", "phthalates", "harmful"],
    'Therapeutic': ["calming", "calm", "nourishing", "nourishes", "soothing", "soothes", "relieves", "relief", "smoothing", "protect", "replenish", "enriched", "restores", "restorative", "restoring", "restore", "rest", "nurturing", "nurture", "resilience", "resilient"],
    'Comorbidity': ["Comorbidity", "diabetic", "eczema", "psoriasis"],
    'Credentials': ["clinically proven", "derm recommended", "proven", "effective", "recommended", "dermatologist approved", "approved", "Leader", "celebrity recommended", "award winning", "experts"],
    'Efficacy': ["blotchiness", "crow's feet", "clinically proven", "derm recommended", "effective", "healthy", "microbiome", "prebiotic", "recommended"],
    'Beauty_Massaging': ["aging", "complex", "dullness", "hydrating", "hydrate", "hydration", "exfoliate", "lines moisturizing", "moisturize", "moisturization", "puffiness", "radiant spots", "strengthen", "texture", "tone", "wrinkles", "brighten", "absorb", "broad spectrum", "protect", "protection non-greasy", "resistant", "resistance"],
    'Ingredient_Massaging': ["Colloidal oatmeal", "Oat", "Oat flour", "Oat kernal", "Dimethicone", "Prebiotic oat", "Shea Butter", "Emollients", "Soy", "Aloe", "Oils", "Lavender", "Ceramides", "Glycerin", "Vitamin E", "Blackberry Extract", "Sunflower Oil", "Almond Oil", "Hydrocortisone", "Cica", "Honey", "Apricot", "Vanilla", "Coconut", "natural shiitake", "southernwood", "dill", "feverfew", "kiwi", "avobenzone", "complex", "enviroguard technology", "lotus", "mineral", "oxybenzone", "SPF", "titanium", "UVA/UVB", "zinc"],
    'Dove': ["confidence", "skin confidence", "self-esteem", "Real Beauty"],
    'CeraVe': ["Essential Ceramides", "Dermatologists", "ceramides", "ceramides 1", "ceramides 3", "ceramides  6-II", "fatty acids", "lipids", "MultiVesicular Emulsion Technology", "MVE Technology", "hydrate", "restore", "replenish"],
    'Aquaphor': ["protective barrier", "healing", "enhance healing", "minimal ingredients", "sensitive skin", "Petrolatum", "dermatologist recommended", "dry", "cracked skin", "restore"],
    'Jergens': ["transform skin", "soft", "smooth", "gorgeous skin", "Natural Glow", "healthier-looking skin", "radiate"],
    'Nivea': ["researchers", "skin types", "skin types (culture, gender, age)", "climate conditions", "cleanse", "nourish", "protect", "gentle", "effective", "effective care"],
    'Vaseline': ["petroleum jelly", "heal", "dry skin", "expert recommended", "Intensive Care", "healing"],
    'Cetaphil': ["gentle skin", "dermatologist recommended", "dermatologist trusted", "sensitive skin", "skin types", "skin conditions", "healthcare professionals", "medical experts"],
    'Gold_Bond': ["physicians", "healing", "cracked skin", "medicated", "therapeutic"],
    'Goddess_Garden': ["Nova Covington", "organic", "plant-based", "pure minerals"],
    'Bare_Republic': ["biodegradable", "clean ingredients", "cruelty free", "trusted performance", "environmentally friendly", "everyday adventures", "eco-active", "titanium dioxide", "zinc oxide"],
    'Supergoop': ["skincare with SPF", "skincare with sunscreen", "experts in SPF", "Holly Thaggard", "Superpowered SPF", "Ounce by ounce", "feel-good"],
    'Neutrogena': ["Dermatologist recommended", "Dermatologist tested", "Neoglucosamine", "skin experts", "hyaluronic acid", "#1", "most awarded", "every day is SUNday", "zinc"],
    'Olay': ["skin scientists", "ageless", "Vitamin B3", "Glycerin", "Retinyl Propionate", "Amino Peptides", "clinical studies", "trusted"],
    'CeraVe': ["Essential Ceramides", "Dermatologists", "ceramides", "ceramides 1", "ceramides 3", "ceramides  6-II", "fatty acids", "lipids", "MultiVesicular Emulsion Technology", "MVE Technology", "hydrate", "restore", "replenish"],
    'Cetaphil': ["gentle skin", "dermatologist recommended", "dermatologist trusted", "sensitive skin", "skin types", "skin conditions", "healthcare professionals", "medical experts"],
    'Burt_Bees': ["True To Nature", "nature's rules", "nature", "hive", "bees", "bee wax"],
    'Garnier': ["skin experts", "natural ingredients", "natural", "antioxidants", "moisture barrier"],
    'Yes_To': ["natural ingredients", "natural", "fruits", "vegetables"],
    'Simple_Skincare': ["Sensitive Skin", "Experts", "clean", "clean ingredients", "Ophthalmologist-tested", "Dermatologist tested", "Dermatologist recommended", "pH Balance"],
    'Babyganics': ["plant-derived", "certified organic", "pediatrician & dermatologist tested", "#marvelousmess", "#babyganics"],
    'Alba_Botanica': ["Do Beautiful", "#dobeautiful", "body-loving products", "100% vegetarian products", "botanical ingredients", "earth friendly"],
    'Hawaiian_Tropic': ["#alohatherapy", "indulgent sun care", "discover the beauty of sun protection", "indulgent protection", "skin nourishing antioxidants", "exotic botanicals"],
    'Sun_Baby_Bum': ["Trust the Bum", "oxybenzone free", "octinoxate free", "reef friendly", "vegan", "gluten free", "cruelty free", "sulfate free", "paraben free"]
    }
    # Transpose the data dictionary to get the correct structure for the DataFrame
    data_transposed = {k: [", ".join(v)] for k, v in data.items()}

    # Create a DataFrame from the transposed data
    df = pd.DataFrame.from_dict(data_transposed, orient='index', columns=['Keywords'])
    
    def categorize_text(text):
        for index, row in df.iterrows():
            keywords = row['Keywords'].split(', ')
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    return index
        return 'Uncategorized'      
        

    user_input = merged_articles    
    selected_columns = ['title', 'summary', 'description', 'content']
    new_df = user_input[selected_columns].astype(str)
    
    # Use .loc to set the 'MergedText' column
    new_df.loc[:, 'MergedText'] = new_df[selected_columns].apply(lambda row: ' '.join(row), axis=1)
    
    results = []

    # Iterate through the records in the 'MergedText' column
    for record in new_df['MergedText']:
        result = str(categorize_text(record))
        results.append(result)
        
    unique_elements, counts = np.unique(results, return_counts=True)
    
    # Check if there is only one category found
    if len(unique_elements) == 1:
        # If there's only one category, you can handle it accordingly.
        # For example, you might want to return that category or handle it differently.
        final_list_5_themes = [unique_elements[0], None, None, None]
    else:
        # Sort the unique elements and counts in descending order
        sorted_indices = np.argsort(-counts)
        sorted_elements = unique_elements[sorted_indices]
        sorted_counts = counts[sorted_indices]

    # Get the 5 most occurring elements (up to 4 elements if available)
    final_list_5_themes = sorted_elements
    
    print(final_list_5_themes)
    
    # Convert the list elements to strings and pad the list with None if there are less than 4 elements
    #final_list_5_themes = [str(theme) for theme in final_list_5_themes]
    #final_list_5_themes += [str(None)] * (4 - len(final_list_5_themes))
    
    
    return final_list_5_themes