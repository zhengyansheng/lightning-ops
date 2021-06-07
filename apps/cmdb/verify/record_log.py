from dictdiffer import diff

from .operate import OperateInstance
from ..models import ChangeRecord


class Record:
    def __init__(self, parent_asset, child_asset, request):
        self.parent_asset = parent_asset
        self.child_asset = child_asset
        self.request = request

    def update_data(self):
        check_data = diff(self.parent_asset.data, self.request.data['data'])
        for tup in list(check_data):
            if hasattr(self, tup[0]):
                getattr(self, tup[0])(tup[1], tup[2])

    def delete_data(self):
        asset_relation = OperateInstance.get_c_asset_relation(self.parent_asset.id)
        if asset_relation:
            for asset_r in asset_relation:
                if asset_r.parent_asset.table_classify.record_log:
                    title = f'删除记录-{asset_r.child_asset.table_classify.name}'
                    msg = f'删除详情: {self.parent_asset.data}'
                    self.record_save(asset_r.parent_asset.id, title, msg, self.get_user())

    def relation(self):
        title = f'新增记录-{self.child_asset.table_classify.name}'
        if self.parent_asset.table_classify.record_log:
            for k, v in self.child_asset.table_classify.fields.fields.items():
                if 'guid' in v:
                    msg = f'新增数据详情: {self.child_asset.data.get(k)}'
                    self.record_save(self.parent_asset.id, title, msg, self.get_user())
                    break

    def un_relation(self):
        parent_asset = self.parent_asset.parent_asset
        child_asset = self.parent_asset.child_asset
        if parent_asset.table_classify.record_log:
            title = f'移除记录-{child_asset.table_classify.name}'
            for k, v in child_asset.table_classify.fields.fields.items():
                if 'guid' in v:
                    msg = f'移除数据详情: {child_asset.data}'
                    self.record_save(parent_asset.id, title, msg, self.get_user())
                    break

    def change(self, field, tup_data):
        msg = f'变更详情: {tup_data[0]} > {tup_data[1]}'

        if self.parent_asset.table_classify.record_log:
            title = f'更新记录-{self.parent_asset.table_classify.name}-{field}'
            self.record_save(self.parent_asset.id, title, msg, self.get_user())

        else:
            asset_child = OperateInstance.get_c_asset_relation(self.parent_asset.id)
            if asset_child:
                for asset_r in asset_child:
                    if asset_r.parent_asset.table_classify.record_log:
                        title = f'更新记录-{asset_r.child_asset.table_classify.name}-{field}'
                        self.record_save(asset_r.parent_asset.id, title, msg, self.get_user())

    def add(self, field, tup_data):
        data, field = tup_data[0][1], tup_data[0][0]
        msg = f'新增数据详情: {data}'
        print(f'字段{field}数据变更: {data}')
        if self.parent_asset.table_classify.record_log:
            title = f'新增数据-{self.parent_asset.table_classify.name}-{field}'
            self.record_save(self.parent_asset.id, title, msg, self.get_user())

        else:
            asset_child = OperateInstance.get_c_asset_relation(self.parent_asset.id)
            if asset_child:
                for asset_r in asset_child:
                    if asset_r.parent_asset.table_classify.record_log:
                        title = f'新增数据-{asset_r.child_asset.table_classify.name}-{field}'
                        self.record_save(asset_r.parent_asset.id, title, msg, self.get_user())

    def remove(self, field, tup_data):
        data, field = tup_data[0][1], tup_data[0][0]
        data = tup_data[0][1]
        msg = f'删除数据详情: {data}'
        print(f'字段{field}数据变更: {data}')
        if self.parent_asset.table_classify.record_log:
            title = f'删除数据-{self.parent_asset.table_classify.name}-{field}'
            self.record_save(self.parent_asset.id, title, msg, self.get_user())

        else:
            asset_child = OperateInstance.get_c_asset_relation(self.parent_asset.id)
            if asset_child:
                for asset_r in asset_child:
                    if asset_r.parent_asset.table_classify.record_log:
                        title = f'删除数据-{asset_r.child_asset.table_classify.name}-{field}'
                        self.record_save(asset_r.parent_asset.id, title, msg, self.get_user())

    def get_user(self):
        try:
            return self.request.user
        except Exception:
            return None

    def record_save(self, d_id, title, detail, operator):
        record_obj = ChangeRecord.objects.create(
            table_data_id=d_id,
            title=title,
            detail=detail,
            operator=operator
        )
        record_obj.save()


def record(func, parent_asset, child_asset, request):
    """ 要执行的函数, 实例  request"""
    r_func = Record(parent_asset, child_asset, request)
    if hasattr(r_func, func):
        getattr(r_func, func)()

#
# x = {
#     "hostname": "www.qq.com",
#     "ip": "1.1.1.1",
#     "xx": "tt"
# }
# y = {
#     "hostname": "www.qq.com",
#     "ip": "1.1.1.111",
#     "yy": "mm"
# }
#
# record('run', x, y)
