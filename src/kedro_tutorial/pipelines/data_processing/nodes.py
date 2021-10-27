import pandas as pd
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark


def _is_true(x):
    return x == "t"


def _parse_percentage(x):
    x = str(x).replace("%", "")
    if x != "None":
        x = float(x) / 100
    else:
        x=None
    return x


def _parse_money(x):
    x = x.replace("$", "").replace(",", "")
    # x = x.astype(float)
    return float(x)


def preprocess_companies(companies: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    """Preprocesses the data for companies.

    Args:
        companies: Raw data.
    Returns:
        Preprocessed data, with `company_rating` converted to a float and
        `iata_approved` converted to boolean.
    """
    # companies.printSchema()
    # companies["iata_approved"] = _is_true(companies["iata_approved"])
    # companies["company_rating"] = _parse_percentage(companies["company_rating"])
    return companies.withColumn("iata_approved", udf(_is_true, StringType())(col("iata_approved"))) \
        .withColumn("company_rating", udf(_parse_percentage, FloatType())(col("company_rating")))
        # .withColumn("company_rating", split(col("iata_approved"),"%")[0].cast(FloatType())/100)


def preprocess_shuttles(shuttles: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    """Preprocesses the data for shuttles.

    Args:
        shuttles: Raw data.
    Returns:
        Preprocessed data, with `price` converted to a float and `d_check_complete`,
        `moon_clearance_complete` converted to boolean.
    """
    # shuttles.printSchema()
    # shuttles["d_check_complete"] = _is_true(shuttles["d_check_complete"])
    # shuttles["moon_clearance_complete"] = _is_true(shuttles["moon_clearance_complete"])
    # shuttles["price"] = _parse_money(shuttles["price"])
    return shuttles\
        .withColumn("d_check_complete", udf(_is_true, StringType())(col("d_check_complete"))) \
        .withColumn("moon_clearance_complete", udf(_is_true, StringType())(col("moon_clearance_complete"))) \
        .withColumn("price", udf(_parse_money, FloatType())(col("price")))
        # .withColumn("price", split(col("price"),"%")[0]).withColumn("price", replace(",","").cast(FloatType()))

def create_model_input_table(
    shuttles: pyspark.sql.DataFrame, companies: pyspark.sql.DataFrame, reviews: pyspark.sql.DataFrame
) -> pyspark.sql.DataFrame:
    """Combines all data to create a model input table.

    Args:
        shuttles: Preprocessed data for shuttles.
        companies: Preprocessed data for companies.
        reviews: Raw data for reviews.
    Returns:
        model input table.

    """
    # rated_shuttles = shuttles.merge(reviews, left_on="id", right_on="shuttle_id")
    # model_input_table = rated_shuttles.merge(
    #     companies, left_on="company_id", right_on="id"
    # )
    # model_input_table = model_input_table.dropna()
    # shuttles.printSchema()
    # reviews.printSchema()
    # companies.printSchema()
    # print(shuttles.count())
    # print(reviews.count())
    # print(companies.count())
    # print(shuttles.join(reviews,on=[col("id")==col("shuttle_id")]).count())
    # print(shuttles.join(reviews,on=[col("id")==col("shuttle_id")]).withColumnRenamed("id","idp").join(companies,on=[col("company_id")==companies.id]).count())
    # print(shuttles.join(reviews,on=[col("id")==col("shuttle_id")]).withColumnRenamed("id","idp").join(companies,on=[col("company_id")==companies.id]).dropna().count())

    return shuttles.join(reviews,on=[col("id")==col("shuttle_id")]).withColumnRenamed("id","idp").join(companies,on=[col("company_id")==companies.id]).dropna()
