from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from manager.models import manager
from django.template import engines
import json

# http://localhost/api/mgr/manager/?action=list
def dispatcher(request):

    # get method
    method = request.method ;

    if method == 'GET':
        request.params = request.GET
    else:
        request.params = json.loads(request.body)

    # get action
    action = request.params['action']
    if action == 'list':
        return list_mgr(request)
    elif action == 'add':
        return add_mgr(request)
    elif action == 'del':
        return del_mgr(request)
    elif action == 'upd':
        return upd_mgr(request)
    else:
        return JsonResponse({
            "ret": "1",
            "msg": f'not support {action}'
        })


def add_mgr(request):

    info = request.params['data']

    record = manager.objects.create(
        name=info.get('name'),
        phone_number = info.get('phone')
    )

    if record:
        ret_code = -1

    return JsonResponse({
        "ret": ret_code,
        "msg": f'add manager {record.id}'
    })

def upd_mgr(request):

    id = request.params['id']

    try:
      manager.objects.get(id=id)
    except manager.DoesNotExist:
      return {
          "ret": -1,
          "msg": f'id {id} doesn\'t exist'
      }

    new_para = request.params['new']
    if 'name' in new_para :
        manager.name = new_para.get('name')
    if 'phone' in new_para:
        manager.phone_number = new_para.get('phone')
    manager.save()

    return {
          "ret": 0,
          "msg": f'id {id} updated'
      }


def del_mgr(request):

    id = request.params['id']

    try:
      manager.objects.get(id=id)
    except manager.DoesNotExist:
      return {
          "ret": -1,
          "msg": f'id {id} doesn\'t exist'
      }

    manager.delete()

    return {
          "ret": 0,
          "msg": f'id {id} deleted'
      }


def list_mgr(request):

    qs = manager.objects.values();

    # filter(?name=xxx)
    filter_name = request.GET.get('name', None)

    if filter_name:
        qs = qs.filter(name=filter_name)

    # retLt = []
    # for mgr in qs :
    #     ret_item = {}
    #     for key, val in mgr.items():
    #         ret_item.update({key: val})
    #     retLt.append(ret_item)
    # =>
    retLt = list(qs)

    return JsonResponse({
        "ret": "0",
        "msg": retLt
    })






manger_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>manager list</title>
</head>
<body>
    <table border="1">
    {% for customer in customers %}
      <tr>
      {% for _, value in customer.items %}
      <td> {{ value }}</td>
      {% endfor %}
      </tr>
    {% endfor %} 
    </table>
</body>
</html>
'''

def list_mgr_http(request):

    qs = manager.objects.values();

    # filter(?name=xxx)
    # http://localhost/manager/getmanagers/?name=mgr1
    filter_name = request.GET.get('name', None)

    if filter_name:
        qs = qs.filter(name=filter_name)

    django_engine = engines['django']
    template = django_engine.from_string(manger_template)
    rendered = template.render({'customers': qs})

    # retStr = '';
    # for mgr in qs :
    #     retStr += '<tr>'
    #     for _, val in mgr.items():
    #         retStr += f'<td>{val}</td>'
    #     retStr += '</tr>'
    # return HttpResponse(manger_template % retStr)

    return HttpResponse(rendered)
