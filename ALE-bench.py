import ale_bench
import ale_bench.utils
import datetime as dt
from openaigent import OpenAIgent 
# Start a new evaluation session
print('starting')
session = ale_bench.start(
    problem_id="ahc001",
    lite_version=False,
    num_workers=8,  # Adjust based on your machine's physical cores
    run_visualization_server=True,
    visualization_server_port=8080
)

# NOTE: While the `session` object contains attributes like `private_seeds`,
# `rank_performance_map`, and `standings`, these (and any other attributes
# prefixed with an underscore, e.g., `_private_inputs`) MUST NOT be accessed
# or used during your experiment to ensure fair evaluation.

# Access problem details
problem = session.problem
problem_statement_md = problem.statement  # Markdown-formatted problem statement
problem_images = problem.statement_images  # Associated images
problem_constraints_obj = problem.constraints  # Structured constraints
#print(problem.statement_images)

my_agent = OpenAIgent(statement=problem_statement_md,
                                 constraints=problem_constraints_obj,
                                 pics=problem_images)

# Example: Constructing an initial prompt for an LLM/LMM
# (Replace with your agent's prompt engineering)
#role = 'You are an optimization expert.'
#my_agent.role_set('You are an optimization expert')
#my_agent.task_set('Analyze the provided problem statement and constraints, and generate a solution written cpp20. Product should be a single block of C++20')
#my_agent.messages_set()
#print('prompt engineering complete')
'''
# Utility for parsing problem statements (e.g., for OpenAI models)
parsed_content = ale_bench.utils.parse_statement(
    problem_statement_md, problem_images, return_openai=True
)
'''
#print('problem parsed')
# Obtain a solution from your LLM/LMM agent

agent_response = my_agent.run()

extracted_code = my_agent.extract_code(agent_response)
detected_language = "cpp20"
# Ensure detected_language is one of: "cpp17", "cpp20", "cpp23", "python", "rust"

#print(type(extracted_code))
# Evaluate against public test cases
public_result = session.public_eval(extracted_code, code_language=detected_language)
print(f"Initial Public Score: {public_result.overall_absolute_score}")


# iterative improvement loop

# Iterative refinement loop (example)
solution_attempts = [(extracted_code, public_result)]
current_best_code = extracted_code

# Define your maximum refinement iterations, e.g., MAX_REFINEMENT_ITERATIONS = 5
'''
for i in range(MAX_REFINEMENT_ITERATIONS):
    feedback_prompt = my_agent.construct_feedback_prompt(
        problem, current_best_code, public_result
    )
    refined_response = my_agent.get_llm_response(feedback_prompt)
    refined_code = my_agent.parse_code_from_response(refined_response)

    if refined_code: # Agent might not always produce new code
        public_result = session.public_eval(refined_code, code_language=detected_language)
        solution_attempts.append((refined_code, public_result))
        # Update current_best_code based on problem's score type (minimize/maximize)
        # (Implementation depends on your agent's strategy)
        current_best_code = my_agent.select_best_code(solution_attempts, problem.metadata.score_type)
    else:
        print(f"Iteration {i+1}: No new code generated.")
        break # Or implement other logic like re-prompting

# Select the final submission based on overall public performance
final_submission_code = my_agent.select_best_code(solution_attempts, problem.metadata.score_type)

# --- Your Agent's Logic Ends ---
'''
# Rank Evaluation
'''
# Evaluate the final submission against private test cases
# Ensure `lite_version=False` during session start for rank and performance calculation.
private_result, final_rank, final_performance = session.private_eval(
    final_submission_code, code_language=detected_language
)
print(f"Final Private Score: {private_result.overall_absolute_score}")
print(f"Rank: {final_rank}, Performance: {final_performance}")
'''
'''
# Monitor resource consumption
print(f"Current Resource Usage: {session.current_resource_usage}")
print(f"Remaining Resources: {session.remaining_resource_usage}")

# Inspect local Rust tool sources (if applicable)
if session.problem.metadata.problem_type == "reactive": # Example condition
    ale_bench.utils.print_dir_tree(session.rust_src_dir)

# Persist session state for later analysis or resumption
session.save("my_ahc001_session.json")

# Explicitly close the session to release resources
session.close()

# To resume a saved session:
# resumed_session = ale_bench.restart("/path/to/my_ahc001_session.json")

# To clear all cached ALE-Bench data (problem data, toolchains):
# ale_bench.clear_cache()
'''