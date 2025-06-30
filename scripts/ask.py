from mods.modeling import get_entry_by_embedding

if __name__ == "__main__":
    query = input("Enter your query: ")
    top_k = int(input("Enter the number of results to return (default 5): ") or 5)
    
    print(f"🔍 Searching for entries similar to: '{query}'")
    results = get_entry_by_embedding(query, top_k)
    
    if results:
        print(f"✅ Found {len(results)} results:")
        for result in results:
            print(f"ID: {result['id']}, Content: {result['content']}, Similarity: {result['similarity']:.4f}")
    else:
        print("❌ No results found.")