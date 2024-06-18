1) PDF processor: As PDF reader/processor I would rather choose PyMuPDF becasue it works well with both images and text, it is faster than the pdfplumber as well.
   Embedder: Even though OpenAI's embedder is state-of-the-art it is too complex, I don't think that installation manuals need that kind of embedders, I consider using BERT for contextual embeddings.
   Vector DB: Pinecone.
   LLM Resopne Generation: I would choose GPT-4 because it has state-of-the-art performance.

2) PDF Documents' Variability: Manuals my have different language and format also based on the tool they might have different structure and it can be challenging to extract relevant information.
   as solution I think I can implement preprocessing step between text/image extraction and embeddings to standardize the information and get rid of unnecessary information.
   High Computational Cost of BERT Embeddings: Creating embeddings can be computationally expensive so I would use pretrained BERT models such as BERT-Base also I would consider caching and parallelization mechanisms.

3) Questions that can be answered - 1) What are the potential causes and solutions for some specific issue in equipment(that could arouse during exploitation).
                                    2) What cleaning and servicing current equipment need and how often in my specific location(by specific location I mean environment specifications).
                                    3) Specific usage scenario descriptions by user and further optimization tips by chatbot.
                                    4) How to perform specific task(for example cooking with wide range of features in nowadays ovens).
                                    5) Installation requirements(what tools the user would be needing).

   Questions that can't be answered - 1) Specific issues with the equipment(even though I considered the question similar to this as a question that can be answered, but some problmes need real-time diagnostics).
                                      2) Comparisons with other similar equipment, chatbot doesn't have access to the external sources.
                                      3) What to do in case of emergency(for example gas leak or house cought on fire), chatbot doesn't have this information in it's db.
                                      4) Modifications(DIY), chatbot cannot provide information for unauthorized modifications to equipment.
                                      5) Compatibility with other equipment, chatbot may not have information about the other equipment.
