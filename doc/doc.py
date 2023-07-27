mongo_doc = '''### Description
The **MongoDB** component allows to interact with MongoDB.

You can set the MongoDB connection in the *config.json* file.

### Configuration

- **Collection name** sets the Mongo collection.
- **Stream or not results** allows to receive the output of a query as a stream or not.

### Input

In order to **insert** new elements to a collection, the component requires single dictionaries or lists of 
dictionaries.

The **query** and **delete** input require the filter of the query. For example:

```
{"label": "science"}
```

Use an empty dictionary if you don't need filters.


'''