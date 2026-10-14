# from crewai.flow.flow import Flow, listen, router, start, or_
from crewai.flow import start, Flow
from pydantic import BaseModel
from crewai.flow.persistence import persist
from fastapi import FastAPI
from flow_practice.api.routes import router
from flow_practice.api.agent_config_routes import router as agent_config_router
from flow_practice.api.task_config_routes import router as task_config_router
from flow_practice.api.crew_config_routes import (
    router as crew_config_router,
)
from flow_practice.api.crew_execution_routes import (
    router as crew_execution_router,
)
from flow_practice.api.llm_config_routes import (
    router as llm_config_router,
)

app = FastAPI(
    title="Employee Intelligence API",
    description="FastAPI + CrewAI + MongoDB",
    version="1.0.0",
)

app.include_router(router)
app.include_router(agent_config_router)
app.include_router(task_config_router)
app.include_router(crew_config_router)
app.include_router(crew_execution_router)
app.include_router(llm_config_router)

@app.get("/")
def root():
    return {
        "message": "Employee Intelligence API is running"
    }

"""
# This is a simple example of a payment flow using CrewAI's Flow framework.
# The flow processes a payment, checks for approval, and handles retries if necessary.
@persist()
class PaymentFlow(Flow[PaymentState]):

    @start()
    def process_payment(self):
        if self.state.amount == 0.0:
            self.state.amount = 10000.0

        self.state.is_approved = self.state.amount < 1000

        print("\n--- process_payment ---")
        print(f"Amount      : ${self.state.amount}")
        print(f"Is approved : {self.state.is_approved}")

        return "Payment processed"

    # Runs after the first attempt AND after every retry attempt
    @router(or_(process_payment, "handle_retry"))
    def check_approval(self, previous_result=None):
        print("\n--- check_approval (@router) ---")
        print(f"Retry count : {self.state.retry_count}")

        if self.state.is_approved:
            print("Routing → approved")
            return "approved"
        elif self.state.retry_count < 3:
            print("Routing → retry")
            return "retry"
        else:
            print("Routing → rejected")
            return "rejected"

    @listen("approved")
    def handle_approval(self):
        result = (
            f"Payment of ${self.state.amount} approved "
            f"after {self.state.retry_count} retries."
        )
        print("\n--- handle_approval ---")
        print(result)
        return result

    @listen("retry")
    def handle_retry(self):
        self.state.retry_count += 1

        print("\n--- handle_retry ---")
        print(f"Retry attempt: {self.state.retry_count}")
        
        # Re-evaluate the payment with the (possibly updated) amount
        self.state.is_approved = self.state.amount < 1000
        print(f"Amount      : ${self.state.amount}")
        print(f"Is approved : {self.state.is_approved}")

        return "retry_payment"

    # Listen to the METHOD handle_retry (not a string label)
    # @listen(handle_retry)
    # def process_retry(self):
    #     print("\n--- process_retry ---")

    #     # Re-evaluate the payment with the (possibly updated) amount
    #     self.state.is_approved = self.state.amount < 1000
    #     print(f"Amount      : ${self.state.amount}")
    #     print(f"Is approved : {self.state.is_approved}")

    #     return "Payment reprocessed"

    @listen("rejected")
    def handle_rejection(self):
        result = (
            f"Payment of ${self.state.amount} rejected "
            f"after {self.state.retry_count} retries."
        )
        print("\n--- handle_rejection ---")
        print(result)
        return result


def kickoff():
    print("=" * 60)
    print("STARTING PAYMENT FLOW")
    print("=" * 60)

    flow = PaymentFlow()
    result = flow.kickoff()

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(f"\nReturned result: {result}")
    print("\nFinal State:")
    print(f"Amount       : ${flow.state.amount}")
    print(f"Is approved  : {flow.state.is_approved}")
    print(f"Retry count  : {flow.state.retry_count}")


if __name__ == "__main__":
    kickoff()

"""