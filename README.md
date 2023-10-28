# LLM-Chat-Backend

## User-side operations 
apps\chat\router.py

## administrators operations
apps\chat\admin_router.py.

The streaming output of the LLMs is implemented through WebSockets in __llm_loader.py__ and __llm_task.py__. 
The logic for loading the knowledge base and historical Q&A is implemented in __llm_handlers.py__. The data structures are defined in schemas.py, and the database operations are defined in __crud.py__.

## To run the application locally, follow these steps:
1. Modify the configuration in the environment file, including the model and MySQL database connection.
2. Run the command "source environment" to read the environment variables.
3. Use pip to install the required external libraries by running "pip install requirements".
4. Start the application by running "python -m uvicorn main:app --port=8002 --host=0.0.0.0 --reload".
5. Afterward, you can access the relevant interfaces, and you can find examples of the interfaces at localhost:8002/doc#.
