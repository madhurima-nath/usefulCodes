from langchain.callbacks.base import BaseCallbackHandler

class BedrockTokenCounter(BaseCallbackHandler):
    def __init__(self, llm):
        self.llm = llm
        self.input_tokens = 0
        self.output_tokens = 0

    def on_llm_start(self, serialized, prompts, **kwargs):
        for p in prompts:
            self.input_tokens += self.llm.get_num_tokens(p)

    def on_llm_end(self, response, **kwargs):
        results = response.flatten()
        for r in results:
            self.output_tokens = self.llm.get_num_tokens(r.generations[0][0].text)


# class BedrockCallCounter(BaseCallbackHandler):
#     def __init__(self):
#         self.nb_calls = 0

#     def on_llm_start(self, serialized, prompts, **kwargs):
#         for _ in prompts:
#             self.nb_calls += 1
            

class AgentMetricsMeasurementTool(BaseCallbackHandler):
    def __init__(self):
        self.nb_calls = 0
        self.total_latency = 0
        self.start_timestamp = None

    def __repr__(self):
        return (
            f"Total calls: {self.nb_calls}\n"
            f"Total latency: {self.total_latency:.2f}s\n"
            f"Avg latency per call: {self.total_latency / self.nb_calls:.2f}s"
        )
    
    def on_llm_start(self, _, prompts, **kwargs):
        self.start_timestamp = time.time()
        for _ in prompts:
            self.nb_calls += 1

    def on_llm_end(self, response, **kwargs):
        self.total_latency += time.time() - self.start_timestamp