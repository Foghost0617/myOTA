from backend.models.message_model import ChatGroup, ChatGroupMember
from backend.models.route_guide import RouteGuide
from backend.models.tourist_route_model import TouristRouteRelation
from backend.models.user import User, Guide, Tourist, TravelAgency, GovAdmin
from sqlalchemy.orm import Session
from typing import List

from backend.schemas.message_schema import CreateGroupChatRequest, CreateGroupChatResponse


class GroupChatService:
        def __init__(self, db: Session):
            self.db = db

        def create_group_chat(self, group_chat: CreateGroupChatRequest) -> CreateGroupChatResponse:
            # 获取创建者信息
            creator_id = group_chat.creator_id
            creator_role = group_chat.creator_role

            # 创建群聊记录
            db_group_chat = ChatGroup(
                name=group_chat.name,
                created_by_id=creator_id,
                created_by_role=creator_role
            )
            self.db.add(db_group_chat)
            self.db.commit()
            self.db.refresh(db_group_chat)

            # 初始化成员列表：先把创建者自己加进去
            member_ids = [creator_id]
            member_roles = [creator_role]

            # 获取合法的其他成员
            extra_member_ids, extra_member_roles = self.get_valid_members(creator_id, creator_role)

            # 合并创建者和其他成员
            member_ids += extra_member_ids
            member_roles += extra_member_roles

            # 添加所有成员到群聊成员表
            self.add_group_members(db_group_chat.id, member_ids, member_roles)

            return CreateGroupChatResponse(
                group_id=db_group_chat.id,
                name=db_group_chat.name,
                creator_id=creator_id,
                creator_role=creator_role,
                member_ids=member_ids,
                member_roles=member_roles
            )

        def get_valid_members(self, creator_id: int, creator_role: int) -> (List[int], List[int]):
            """根据创建者的角色获取可以拉的群成员"""
            valid_member_ids = []
            valid_member_roles = []

            if creator_role == 3:  # 旅社
                agency_id = self.db.query(TravelAgency).filter(TravelAgency.id == creator_id).first().id
                print("旅社id：",agency_id)
                guides = self.db.query(Guide).filter(Guide.agency_id == agency_id).all()
                valid_member_ids = [guide.user_id for guide in guides]
                valid_member_roles = [2] * len(valid_member_ids)

            elif creator_role == 4:  # 文旅局
                travel_agencies = self.db.query(TravelAgency).all()
                valid_member_ids = [agency.user_id for agency in travel_agencies]
                valid_member_roles = [3] * len(valid_member_ids)
            elif creator_role == 2:  # 导游
                assigned_route_ids = self.db.query(RouteGuide.route_id).filter(RouteGuide.guide_id == creator_id).all()
                assigned_route_ids = [route_id[0] for route_id in assigned_route_ids]
                tourists = self.db.query(TouristRouteRelation).filter(
                    TouristRouteRelation.route_id.in_(assigned_route_ids)).all()
                valid_member_ids = [tourist.tourist_id for tourist in tourists]
                valid_member_roles = [1] * len(valid_member_ids)

            return valid_member_ids, valid_member_roles

        def add_group_members(self, group_id: int, member_ids: List[int], member_roles: List[int]):
            """添加群聊成员"""
            for member_id, member_role in zip(member_ids, member_roles):
                db_member = ChatGroupMember(
                    group_id=group_id,
                    user_id=member_id,
                    user_role=member_role
                )
                self.db.add(db_member)
            self.db.commit()

        # 查询某用户所在的所有群聊
        def get_user_groups(self, user_id: int):
            # 查出这个用户在 chat_group_members 表里的所有 group_id
            group_member_records = self.db.query(ChatGroupMember.group_id).filter(
                ChatGroupMember.user_id == user_id
            ).all()

            # 提取 group_id 列表
            group_ids = [record.group_id for record in group_member_records]

            if not group_ids:
                return []  # 这个用户不在任何群聊中

            # 根据 group_ids 查 chat_groups 表，拿群聊信息
            groups = self.db.query(ChatGroup).filter(
                ChatGroup.id.in_(group_ids)
            ).all()

            return groups


