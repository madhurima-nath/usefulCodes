from __future__ import annotations

from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union,
)

from langchain_core.callbacks import (
    Callbacks,
)
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.pydantic_v1 import root_validator
from langchain_core.runnables import Runnable
from langchain.agents.agent import (
    AgentExecutor,
    RunnableAgent,
)

class RunnableBatchAgent(RunnableAgent):
    def plan(
            self,
            intermediate_steps: List(Tuple[AgentAction, str]),
            callbacks: Callbacks = None,
            **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """
        Based on past history and current inputs, decide what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with the observations.
            callbacks: Callbacks to run.
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """

        # Overriding the default method is NOT use streaming
        # This will use Bedrock's InvokeModel API instead of the
        # InvokeModelWithResponseStream API which might be
        # causing the ThrottlingException error
        inputs = {**kwargs, **{"intermediate_steps": intermediate_steps}}
        return self.runnable.invoke(inputs, config={"callbacks": callbacks})
    

class AgentExecutorBatch(AgentExecutor):
    @root_validator(pre=True)
    def validate_runnable_agent(cls, values: Dict) -> Dict:
        """
        convert runnable to agent if passed in.
        """
        agent = values["agent"]
        if isinstance(agent, Runnable):
            try:
                output_type = agent.OutputType
            except Exception as _:
                multi_action = False
        else:
            multi_action = output_type == Union[List[AgentAction], AgentFinish]

        if multi_action:
            raise NotImplementedError(
                "RunnableMultiActionAgent agent wasn't customized for batch requests"
            )
        else:
            values["agent"] = RunnableBatchAgent(runnable=agent)
        return values