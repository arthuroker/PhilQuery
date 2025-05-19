# build_index.py

import os
from dotenv import load_dotenv
from .indexing import load_and_chunk_with_metadata, build_faiss_index, save_index, section_chunker

# Load .env in case you want to test locally
load_dotenv()

def get_sources():
    data_dir = "data"
    sources = [
        {
            "filepath": os.path.join(data_dir, "The Social Contract by John Jacques Rousseau.txt"),
            "metadata": {
                "source_title": "The Social Contract", 
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0004"
            },
            "section_headers": [
                "SUBJECT OF THE FIRST BOOK", "THE FIRST SOCIETIES", "THE RIGHT OF THE STRONGEST",
                "SLAVERY", "THAT WE MUST ALWAYS GO BACK TO A FIRST CONVENTION", "THE SOCIAL COMPACT",
                "THE SOVEREIGN", "THE CIVIL STATE", "REAL PROPERTY", "BOOK",
                "THAT SOVEREIGNTY IS INALIENABLE", "THAT SOVEREIGNTY IS INDIVISIBLE",
                "WHETHER THE GENERAL WILL IS FALLIBLE", "THE LIMITS OF THE SOVEREIGN POWER",
                "THE RIGHT OF LIFE AND DEATH", "LAW", "THE LEGISLATOR", "THE PEOPLE",
                "THE PEOPLE", "THE PEOPLE", "THE VARIOUS SYSTEMS OF LEGISLATION",
                "THE DIVISION OF THE LAWS", "BOOK", "GOVERNMENT IN GENERAL",
                "THE CONSTITUENT PRINCIPLE IN THE VARIOUS FORMS OF GOVERNMENT",
                "THE DIVISION OF GOVERNMENTS", "DEMOCRACY", "ARISTOCRACY", "MONARCHY",
                "MIXED GOVERNMENTS", "THAT ALL FORMS OF GOVERNMENT DO NOT SUIT ALL COUNTRIES",
                "THE MARKS OF A GOOD GOVERNMENT", 
                "THE ABUSE OF GOVERNMENT AND ITS TENDENCY TO DEGENERATE",
                "THE DEATH OF THE BODY POLITIC", "HOW THE SOVEREIGN AUTHORITY MAINTAINS ITSELF",
                "DEPUTIES OR REPRESENTATIVES", 
                "THAT THE INSTITUTION OF GOVERNMENT IS NOT A CONTRACT",
                "THE INSTITUTION OF GOVERNMENT", "HOW TO CHECK THE USURPATIONS OF GOVERNMENT",
                "BOOK", "THAT THE GENERAL WILL IS INDESTRUCTIBLE", "VOTING", "ELECTIONS",
                "THE ROMAN COMITIA", "THE TRIBUNATE", "THE DICTATORSHIP", "THE CENSORSHIP",
                "CIVIL RELIGION", "CONCLUSION"
            ]
        },
        {
            "filepath": os.path.join(data_dir, "A Discourse on Political Economy by John Jacques Rousseau.txt"),
            "metadata": {
                "source_title": "A Discourse on Political Economy",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0002"
            },
            "section_headers": ["A DISCOURSE ON POLITICAL ECONOMY"]
        },
        {
            "filepath": os.path.join(data_dir, "A Discourse on the Origin and Basis of Inequality Among Men by John Jacques Rousseau .txt"),
            "metadata": {
                "source_title": "A Discourse on the Origin and Basis of Inequality Among Men",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0003"
            },
            "section_headers": [
                "A DISCOURSE ON THE ORIGIN OF INEQUALITY",
                "A DISSERTATION ON THE ORIGIN AND FOUNDATION OF THE INEQUALITY OF MANKIND",
                "THE FIRST PART", "THE SECOND PART"
            ]
        },
        {
            "filepath": os.path.join(data_dir, "A Discourse on the Sciences and Arts by John Jacques Rousseau .txt"),
            "metadata": {
                "source_title": "A Discourse on the Sciences and Arts",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0001"
            },
            "section_headers": [
                "A DISCOURSE ON THE ARTS AND SCIENCES", "PREFACE",
                "MORAL EFFECTS OF THE ARTS AND SCIENCES", 
                "THE FIRST PART", "THE SECOND PART"
            ]
        }
    ]
    return sources

def main():
    print("📚 Building index for Rousseau...")

    data_dir = "data"
    sources = [
        {
            "filepath": os.path.join(data_dir, "The Social Contract by John Jacques Rousseau.txt"),
            "metadata": {
                "source_title": "The Social Contract",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0004"
            },
            "section_headers": [
                "SUBJECT OF THE FIRST BOOK",
                "THE FIRST SOCIETIES",
                "THE RIGHT OF THE STRONGEST",
                "SLAVERY",
                "THAT WE MUST ALWAYS GO BACK TO A FIRST CONVENTION",
                "THE SOCIAL COMPACT",
                "THE SOVEREIGN",
                "THE CIVIL STATE",
                "REAL PROPERTY",
                "BOOK",
                "THAT SOVEREIGNTY IS INALIENABLE",
                "THAT SOVEREIGNTY IS INDIVISIBLE",
                "WHETHER THE GENERAL WILL IS FALLIBLE",
                "THE LIMITS OF THE SOVEREIGN POWER",
                "THE RIGHT OF LIFE AND DEATH",
                "LAW",
                "THE LEGISLATOR",
                "THE PEOPLE",
                "THE PEOPLE",
                "THE PEOPLE",
                "THE VARIOUS SYSTEMS OF LEGISLATION",
                "THE DIVISION OF THE LAWS",
                "BOOK",
                "GOVERNMENT IN GENERAL",
                "THE CONSTITUENT PRINCIPLE IN THE VARIOUS FORMS OF GOVERNMENT",
                "THE DIVISION OF GOVERNMENTS",
                "DEMOCRACY",
                "ARISTOCRACY",
                "MONARCHY",
                "MIXED GOVERNMENTS",
                "THAT ALL FORMS OF GOVERNMENT DO NOT SUIT ALL COUNTRIES",
                "THE MARKS OF A GOOD GOVERNMENT",
                "THE ABUSE OF GOVERNMENT AND ITS TENDENCY TO DEGENERATE",
                "THE DEATH OF THE BODY POLITIC",
                "HOW THE SOVEREIGN AUTHORITY MAINTAINS ITSELF",
                "DEPUTIES OR REPRESENTATIVES",
                "THAT THE INSTITUTION OF GOVERNMENT IS NOT A CONTRACT",
                "THE INSTITUTION OF GOVERNMENT",
                "HOW TO CHECK THE USURPATIONS OF GOVERNMENT",
                "BOOK",
                "THAT THE GENERAL WILL IS INDESTRUCTIBLE",
                "VOTING",
                "ELECTIONS",
                "THE ROMAN COMITIA",
                "THE TRIBUNATE",
                "THE DICTATORSHIP",
                "THE CENSORSHIP",
                "CIVIL RELIGION",
                "CONCLUSION"
            ]
        },
                {
            "filepath": os.path.join(data_dir, "A Discourse on Political Economy by John Jacques Rousseau.txt"),
            "metadata": {
                "source_title": "A Discourse on Political Economy",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0002"
            },
            "section_headers": [
                    "A DISCOURSE ON POLITICAL ECONOMY",
                ]
        },
                {
            "filepath": os.path.join(data_dir, "A Discourse on the Origin and Basis of Inequality Among Men by John Jacques Rousseau .txt"),
            "metadata": {
                "source_title": "A Discourse on the Origin and Basis of Inequality Among Men",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0003"
            },
                "section_headers": [
                    "A DISCOURSE ON THE ORIGIN OF INEQUALITY",
                    "A DISSERTATION ON THE ORIGIN AND FOUNDATION OF THE INEQUALITY OF MANKIND",
                    "THE FIRST PART",
                    "THE SECOND PART",
                ]
        },
                {
            "filepath": os.path.join(data_dir, "A Discourse on the Sciences and Arts by John Jacques Rousseau .txt"),
            "metadata": {
                "source_title": "A Discourse on the Sciences and Arts",
                "author": "Jean-Jacques Rousseau",
                "url": "https://www.gutenberg.org/cache/epub/46333/pg46333-images.html#link2H_4_0001"
            },

            "section_headers": [
                    "A DISCOURSE ON THE ARTS AND SCIENCES",
                    "PREFACE",
                    "MORAL EFFECTS OF THE ARTS AND SCIENCES",
                    "THE FIRST PART",
                    "THE SECOND PART",


                ]
        },
    ]

    all_chunks = []

    for src in sources:

        chunks = section_chunker(
            filepath=src["filepath"],
            metadata=src["metadata"],
            section_headers=src["section_headers"],
            chunk_size_tokens=450
        )
        all_chunks.extend(chunks)

    if not all_chunks:
        print("❌ No chunks found. Exiting.")
        return
    

    print("\nStarting de-duplication process...")
    unique_chunks_list = []
    seen_texts = set() 

    for chunk in all_chunks:
        chunk_text = chunk.get('text', '').strip()

        if chunk_text and chunk_text not in seen_texts:
            unique_chunks_list.append(chunk)
            seen_texts.add(chunk_text)


    print(f"\nOriginal chunk count: {len(all_chunks)}")
    print(f"Unique chunk count after de-duplication: {len(unique_chunks_list)}")



    index, chunk_store = build_faiss_index(unique_chunks_list)



    if index is not None and chunk_store is not None:
        save_index(index, chunk_store, filename_prefix="rousseau_works")
        print(f"✅ Saved index and metadata for {len(chunk_store)} chunks.")
    else:
        print("❌ Failed to build index.")

if __name__ == "__main__":
    main()