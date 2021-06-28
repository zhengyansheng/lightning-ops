from ..models import TableData, ChangeRecord
from .operate import OperateInstance
from dictdiffer import diff


class Record:
    def __init__(self, parent_asset, child_asset, request):
        self.parent_asset = parent_asset
        self.child_asset = child_asset
        self.request = request

    def update_data(self):
        check_data = diff(self.child_asset.data, self.request.data["data"])
        check_data = list(check_data)
        tup_dic = {
            "change": [],
            "add": [],
            "remove": [],
        }
        for tup in check_data:
            # [('change', 'name', ('eth331', 'eth3311')), ('change', 'test', ('11131', '111311'))]
            # [('add', '', [('33', 33)]), ('remove', '', [('22', '22')])]
            if tup[0] == "change":
                tup_dic[tup[0]].append(
                    f"属性<{tup[1]}>: 旧值:{tup[2][0]} -> 新值: {tup[2][1]}"
                )
            elif tup[0] == "add":
                tup_dic[tup[0]].append(f"属性: {tup[2][0][0]} -> 值: {tup[2][0][1]}")
            elif tup[0] == "remove":
                tup_dic[tup[0]].append(f"属性: {tup[2][0][0]} -> 值: {tup[2][0][1]}")
        for k, v in tup_dic.items():
            if v:
                if hasattr(self, k):
                    getattr(self, k)(v)
        # if hasattr(self, tup[0]):
        #     getattr(self, tup[0])(tup[1], tup[2])

    def delete_data(self):
        asset_relation = OperateInstance.get_c_asset_relation(self.parent_asset.id)
        if asset_relation:
            for asset_r in asset_relation:
                if asset_r.parent_asset.table_classify.record_log:
                    title = f"删除记录-{asset_r.child_asset.table_classify.name}"
                    msg = f"删除详情: {self.parent_asset.data}"
                    self.record_save(
                        asset_r.parent_asset.id, title, msg, self.get_user()
                    )

    def relation(self):
        title, msg = self.get_msg("新增记录")
        if msg and title:
            if self.child_asset.table_classify.record_log:
                self.record_save(self.child_asset.id, title, msg, self.get_user())
            if self.parent_asset.table_classify.record_log:
                self.record_save(self.parent_asset.id, title, msg, self.get_user())

    def un_relation(self):
        title, msg = self.get_msg("移除记录")
        if msg and title:
            if self.child_asset.table_classify.record_log:
                self.record_save(self.child_asset.id, title, msg, self.get_user())
            if self.parent_asset.table_classify.record_log:
                self.record_save(self.parent_asset.id, title, msg, self.get_user())

    def get_msg(self, title_mag):
        title, msg = None, None
        for k, v in self.child_asset.table_classify.fields.fields.items():
            if v.get("guid"):
                msg = f"{self.child_asset.data}"
                title = f"{title_mag}-{self.child_asset.table_classify.name}-{self.child_asset.data.get(k)}"
                break
        if msg and title:
            return title, msg
        return None, None

    def change(self, value):
        title, _ = self.get_msg("变更记录")
        value = """\n""".join(value)
        if self.child_asset.table_classify.record_log:
            self.record_save(self.child_asset.id, title, value, self.get_user())

        asset_child = OperateInstance.get_c_asset_relation(self.child_asset.id)
        if asset_child:
            for asset_r in asset_child:
                if asset_r.parent_asset.table_classify.record_log:
                    self.record_save(
                        asset_r.parent_asset.id, title, value, self.get_user()
                    )

    def add(self, value):
        title, _ = self.get_msg("属性新增")
        value = """\n""".join(value)
        if self.child_asset.table_classify.record_log:
            self.record_save(self.child_asset.id, title, value, self.get_user())

        asset_child = OperateInstance.get_c_asset_relation(self.child_asset.id)
        if asset_child:
            for asset_r in asset_child:
                if asset_r.parent_asset.table_classify.record_log:
                    self.record_save(
                        asset_r.parent_asset.id, title, value, self.get_user()
                    )

    def remove(self, value):
        title, _ = self.get_msg("属性移除")
        value = """\n""".join(value)

        if self.child_asset.table_classify.record_log:
            self.record_save(self.child_asset.id, title, value, self.get_user())

        asset_child = OperateInstance.get_c_asset_relation(self.child_asset.id)
        if asset_child:
            for asset_r in asset_child:
                if asset_r.parent_asset.table_classify.record_log:
                    self.record_save(
                        asset_r.parent_asset.id, title, value, self.get_user()
                    )

    def get_user(self):
        try:
            return str(self.request.user)
        except Exception:
            return None

    def record_save(self, d_id, title, detail, operator):
        record_obj = ChangeRecord.objects.create(
            table_data_id=d_id, title=title, detail=detail, operator=operator
        )
        record_obj.save()


def record(func, parent_asset, child_asset, request):
    """要执行的函数, 实例  request"""
    r_func = Record(parent_asset, child_asset, request)
    if hasattr(r_func, func):
        getattr(r_func, func)()
