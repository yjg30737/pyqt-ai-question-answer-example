import threading
from transformers import AutoTokenizer, pipeline


def getAnswer(model_class, model_name, question, context, tokenizer=None):
    result = None
    event = threading.Event()

    def execute_thread():
        nonlocal result
        model = model_class.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
        QA_input = {
            'question': question,
            'context': context
        }

        result = nlp(QA_input)
        event.set()  # Signal that the thread has completed

    thread = threading.Thread(target=execute_thread)
    thread.start()

    # Wait for the thread to complete and retrieve the result
    event.wait()
    return result
