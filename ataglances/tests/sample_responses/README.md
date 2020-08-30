# Sample Responses

These are samples of raw "JSON" responses generated using:

```python
>>> from ataglances import glance
>>> import yaml
>>> response = glance.request_data(server, endpoint)
>>> yaml.dump(response, open(f'{server}_{endpoint}.yaml', 'w')
```
which were then condensed by hand.
