from kedro.pipeline import Pipeline, node

from .nodes import preprocess_companies, preprocess_shuttles, create_model_input_table

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=preprocess_companies,
                inputs="companies",
                outputs="preprocessed_companies",
                name="preprocess_companies_node",
            ),
            node(
                func=lambda x: x,
                inputs="shuttles",
                outputs="shuttles_csv@pandas",
                name="pandas_to_spark",
            ),
            node(
                func=preprocess_shuttles,
                inputs="shuttles_csv@spark",
                outputs="preprocessed_shuttles",
                name="preprocess_shuttles_node",
            ),
           node(
               func=create_model_input_table,
               inputs=["preprocessed_shuttles", "preprocessed_companies", "reviews"],
               outputs="model_input_table",
               name="create_model_input_table_node",
	   ),
        ]
    )
