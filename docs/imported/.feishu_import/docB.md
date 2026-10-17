
> 📌 本文档为《any-sync 协议 Protobuf 接口参考》系列第 2 篇：消息结构 · 数据格式（any-block：changes / events / models / snapshot）。

## 三、消息结构

> 按文件分组；嵌套消息用 `Parent.Child` 点路径表示。`oneof` 行无字段编号。


### any-block/format/v1/proto/changes.proto

#### `Change`

> the element of change tree used to store and internal apply smartBlock history

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 3 | `repeated Content` | `content` | set of actions to apply |
| 4 | `repeated Snapshot` | `snapshot` | snapshot - when not null, the Content will be ignored |
| 6 | `repeated FileKeys` | `fileKeys` | file keys related to changes content |
| 7 | `repeated int64` | `timestamp` | creation timestamp |
| 8 | `repeated uint32` | `version` | version of business logic |
| 9 | `repeated uint32` | `changeType` | business-level type of change applied to object |

#### `Change.BlockCreate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `targetId` |  |
| 2 | `repeated anytype.model.Block.Position` | `position` |  |
| 3 | `repeated anytype.model.Block` | `blocks` |  |

#### `Change.BlockDuplicate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `targetId` |  |
| 2 | `repeated anytype.model.Block.Position` | `position` |  |
| 3 | `repeated string` | `ids` |  |

#### `Change.BlockMove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `targetId` |  |
| 2 | `repeated anytype.model.Block.Position` | `position` |  |
| 3 | `repeated string` | `ids` |  |

#### `Change.BlockRemove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |

#### `Change.BlockUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 2 | `repeated Event.Message` | `events` |  |

#### `Change.Content`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) value | |  |

#### `Change.DetailsSet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| 2 | `repeated google.protobuf.Value` | `value` |  |

#### `Change.DetailsUnset`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |

#### `Change.DeviceAdd`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.DeviceInfo` | `device` |  |

#### `Change.DeviceUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `name` |  |

#### `Change.FileKeys`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `hash` |  |
| 2 | `repeated map<string, string>` | `keys` |  |

#### `Change.NotificationCreate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Notification` | `notification` |  |

#### `Change.NotificationUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Notification.Status` | `status` |  |

#### `Change.ObjectTypeAdd`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated string` | `key` |  |

#### `Change.ObjectTypeRemove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated string` | `key` |  |

#### `Change.OriginalCreatedTimestampSet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int64` | `ts` |  |

#### `Change.RelationAdd`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.RelationLink` | `relationLinks` |  |

#### `Change.RelationRemove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `relationKey` |  |

#### `Change.SetFileInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated model.FileInfo` | `fileInfo` |  |

#### `Change.Snapshot`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated map<string, string>` | `logHeads` | logId -> lastChangeId |
| 2 | `repeated anytype.model.SmartBlockSnapshotBase` | `data` | snapshot data |
| 3 | `repeated FileKeys` | `fileKeys` | all file keys related to doc |

#### `Change.StoreKeySet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `path` |  |
| 2 | `repeated google.protobuf.Value` | `value` |  |

#### `Change.StoreKeyUnset`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `path` |  |

#### `Change.StoreSliceUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| — | (oneof) operation | |  |

#### `Change.StoreSliceUpdate.Add`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated string` | `ids` |  |

#### `Change.StoreSliceUpdate.Move`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated string` | `ids` |  |

#### `Change.StoreSliceUpdate.Remove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |

#### `ChangeNoSnapshot`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 3 | `repeated Change.Content` | `content` | set of actions to apply |
| 6 | `repeated Change.FileKeys` | `fileKeys` | file keys related to changes content |
| 7 | `repeated int64` | `timestamp` | creation timestamp |
| 8 | `repeated uint32` | `version` | version of business logic |
| 9 | `repeated uint32` | `changeType` | business-level type of change applied to object |

#### `DocumentCreate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `collection` |  |
| 2 | `repeated string` | `documentId` |  |
| 3 | `repeated string` | `value` | json |

#### `DocumentDelete`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `collection` |  |
| 2 | `repeated string` | `documentId` |  |

#### `DocumentModify`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `collection` |  |
| 2 | `repeated string` | `documentId` |  |
| 4 | `repeated KeyModify` | `keys` |  |

#### `KeyModify`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `keyPath` | key path; example: [user, email] |
| 3 | `repeated ModifyOp` | `modifyOp` | modify op: set, unset, inc, etc. |
| 4 | `repeated string` | `modifyValue` | json value; example: '"new@example.com"' |

#### `StoreChange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated StoreChangeContent` | `changeSet` |  |

#### `StoreChangeContent`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) change | |  |


### any-block/format/v1/proto/events.proto

#### `Event`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Message` | `messages` |  |
| 2 | `repeated string` | `contextId` |  |
| 3 | `repeated anytype.model.Account` | `initiator` |  |
| 4 | `repeated string` | `traceId` |  |

#### `Event.Account`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Account.Config`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Account.Config.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Account.Config` | `config` |  |
| 2 | `repeated anytype.model.Account.Status` | `status` |  |

#### `Event.Account.Details`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `profileId` |  |
| 2 | `repeated google.protobuf.Struct` | `details` |  |

#### `Event.Account.LinkChallenge`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `challenge` |  |
| 2 | `repeated ClientInfo` | `clientInfo` |  |
| 3 | `repeated model.Account.Auth.LocalApiScope` | `scope` |  |

#### `Event.Account.LinkChallenge.ClientInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `processName` |  |
| 2 | `repeated string` | `processPath` |  |
| 4 | `repeated string` | `name` |  |
| 3 | `repeated bool` | `signatureVerified` |  |

#### `Event.Account.LinkChallengeHide`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Account.Show`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int32` | `index` |  |

#### `Event.Account.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Account.Config` | `config` |  |
| 2 | `repeated anytype.model.Account.Status` | `status` |  |

#### `Event.Block`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Add`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block` | `blocks` |  |

#### `Event.Block.Dataview`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Dataview.GroupOrderUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.GroupOrder` | `groupOrder` |  |

#### `Event.Block.Dataview.IsCollectionSet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated bool` | `value` |  |

#### `Event.Block.Dataview.ObjectOrderUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `viewId` |  |
| 3 | `repeated string` | `groupId` |  |
| 4 | `repeated SliceChange` | `sliceChanges` |  |

#### `Event.Block.Dataview.OldRelationDelete`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `relationKey` |  |

#### `Event.Block.Dataview.OldRelationSet`

> sent when the dataview relation has been changed or added

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `relationKey` |  |
| 3 | `repeated anytype.model.Relation` | `relation` |  |

#### `Event.Block.Dataview.RelationDelete`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `relationKeys` |  |

#### `Event.Block.Dataview.RelationSet`

> sent when the dataview relation has been changed or added

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |

#### `Event.Block.Dataview.SliceChange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SliceOperation` | `op` |  |
| 2 | `repeated string` | `ids` |  |
| 3 | `repeated string` | `afterId` |  |

#### `Event.Block.Dataview.SourceSet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `source` |  |

#### `Event.Block.Dataview.TargetObjectIdSet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `targetObjectId` |  |

#### `Event.Block.Dataview.ViewDelete`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `viewId` |  |

#### `Event.Block.Dataview.ViewOrder`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `viewIds` |  |

#### `Event.Block.Dataview.ViewSet`

> sent when the view have been changed or added

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 3 | `repeated anytype.model.Block.Content.Dataview.View` | `view` | doesn't switch the active view in the middle |

#### `Event.Block.Dataview.ViewUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `viewId` |  |
| 3 | `repeated Filter` | `filter` |  |
| 4 | `repeated Relation` | `relation` |  |
| 5 | `repeated Sort` | `sort` |  |
| 6 | `repeated Fields` | `fields` |  |

#### `Event.Block.Dataview.ViewUpdate.Fields`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block.Content.Dataview.View.Type` | `type` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated string` | `coverRelationKey` |  |
| 4 | `repeated bool` | `hideIcon` |  |
| 6 | `repeated bool` | `coverFit` |  |
| 7 | `repeated string` | `groupRelationKey` |  |
| 16 | `repeated string` | `endRelationKey` |  |
| 8 | `repeated bool` | `groupBackgroundColors` |  |
| 9 | `repeated int32` | `pageLimit` |  |
| 17 | `repeated bool` | `wrapContent` | within the view |
| 18 | `repeated anytype.model.Block.Content.Dataview.View.ListSize` | `listSize` |  |
| 19 | `repeated bool` | `alternateRows` |  |

#### `Event.Block.Dataview.ViewUpdate.Filter`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) operation | |  |

#### `Event.Block.Dataview.ViewUpdate.Filter.Add`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Filter` | `items` |  |

#### `Event.Block.Dataview.ViewUpdate.Filter.Move`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated string` | `ids` |  |

#### `Event.Block.Dataview.ViewUpdate.Filter.Remove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Dataview.ViewUpdate.Filter.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Filter` | `item` |  |

#### `Event.Block.Dataview.ViewUpdate.Relation`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) operation | |  |

#### `Event.Block.Dataview.ViewUpdate.Relation.Add`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Relation` | `items` |  |

#### `Event.Block.Dataview.ViewUpdate.Relation.Move`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated string` | `ids` |  |

#### `Event.Block.Dataview.ViewUpdate.Relation.Remove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Dataview.ViewUpdate.Relation.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Relation` | `item` |  |

#### `Event.Block.Dataview.ViewUpdate.Sort`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) operation | |  |

#### `Event.Block.Dataview.ViewUpdate.Sort.Add`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Sort` | `items` |  |

#### `Event.Block.Dataview.ViewUpdate.Sort.Move`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` |  |
| 2 | `repeated string` | `ids` |  |

#### `Event.Block.Dataview.ViewUpdate.Sort.Remove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Dataview.ViewUpdate.Sort.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Sort` | `item` |  |

#### `Event.Block.Delete`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.FilesUpload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `blockId` |  |
| 2 | `repeated string` | `filePath` |  |

#### `Event.Block.Fill`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Align`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Align` | `align` |  |

#### `Event.Block.Fill.BackgroundColor`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `backgroundColor` |  |

#### `Event.Block.Fill.Bookmark`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Url` | `url` |  |
| 3 | `repeated Title` | `title` |  |
| 4 | `repeated Description` | `description` |  |
| 5 | `repeated ImageHash` | `imageHash` |  |
| 6 | `repeated FaviconHash` | `faviconHash` |  |
| 7 | `repeated Type` | `type` |  |
| 8 | `repeated TargetObjectId` | `targetObjectId` |  |

#### `Event.Block.Fill.Bookmark.Description`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Bookmark.FaviconHash`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Bookmark.ImageHash`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Bookmark.TargetObjectId`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Bookmark.Title`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Bookmark.Type`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Bookmark.Url`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.ChildrenIds`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `childrenIds` |  |

#### `Event.Block.Fill.DatabaseRecords`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `records` |  |

#### `Event.Block.Fill.Details`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `details` |  |

#### `Event.Block.Fill.Div`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Style` | `style` |  |

#### `Event.Block.Fill.Div.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Fields`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `fields` |  |

#### `Event.Block.Fill.File`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Type` | `type` |  |
| 3 | `repeated State` | `state` |  |
| 4 | `repeated Mime` | `mime` |  |
| 5 | `repeated Hash` | `hash` |  |
| 6 | `repeated Name` | `name` |  |
| 7 | `repeated Size` | `size` |  |
| 8 | `repeated Style` | `style` |  |

#### `Event.Block.Fill.File.Hash`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.Mime`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.Name`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.Size`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.State`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.Type`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.File.Width`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Link`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated TargetBlockId` | `targetBlockId` |  |
| 3 | `repeated Style` | `style` |  |
| 4 | `repeated Fields` | `fields` |  |

#### `Event.Block.Fill.Link.Fields`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Link.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Link.TargetBlockId`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Restrictions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Restrictions` | `restrictions` |  |

#### `Event.Block.Fill.Text`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Text` | `text` |  |
| 3 | `repeated Style` | `style` |  |
| 4 | `repeated Marks` | `marks` |  |
| 5 | `repeated Checked` | `checked` |  |
| 6 | `repeated Color` | `color` |  |

#### `Event.Block.Fill.Text.Checked`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Text.Color`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Text.Marks`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Text.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Fill.Text.Text`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.MarksInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block.Content.Text.Mark.Type` | `marksInRange` |  |

#### `Event.Block.Set`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Align`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Align` | `align` |  |

#### `Event.Block.Set.BackgroundColor`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `backgroundColor` |  |

#### `Event.Block.Set.Bookmark`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Url` | `url` |  |
| 3 | `repeated Title` | `title` |  |
| 4 | `repeated Description` | `description` |  |
| 5 | `repeated ImageHash` | `imageHash` |  |
| 6 | `repeated FaviconHash` | `faviconHash` |  |
| 7 | `repeated Type` | `type` |  |
| 8 | `repeated TargetObjectId` | `targetObjectId` |  |
| 9 | `repeated State` | `state` |  |

#### `Event.Block.Set.Bookmark.Description`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.FaviconHash`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.ImageHash`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.State`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.TargetObjectId`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.Title`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.Type`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Bookmark.Url`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.ChildrenIds`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `childrenIds` |  |

#### `Event.Block.Set.Div`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Style` | `style` |  |

#### `Event.Block.Set.Div.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Fields`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `fields` |  |

#### `Event.Block.Set.File`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Type` | `type` |  |
| 3 | `repeated State` | `state` |  |
| 4 | `repeated Mime` | `mime` |  |
| 5 | `repeated Hash` | `hash` |  |
| 6 | `repeated Name` | `name` |  |
| 7 | `repeated Size` | `size` |  |
| 8 | `repeated Style` | `style` |  |
| 9 | `repeated TargetObjectId` | `targetObjectId` |  |

#### `Event.Block.Set.File.Hash`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.Mime`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.Name`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.Size`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.State`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.TargetObjectId`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.Type`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.File.Width`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Latex`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Text` | `text` |  |
| 3 | `repeated Processor` | `processor` |  |

#### `Event.Block.Set.Latex.Processor`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block.Content.Latex.Processor` | `value` |  |

#### `Event.Block.Set.Latex.Text`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Link`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated TargetBlockId` | `targetBlockId` |  |
| 3 | `repeated Style` | `style` |  |
| 4 | `repeated Fields` | `fields` |  |
| 5 | `repeated IconSize` | `iconSize` |  |
| 6 | `repeated CardStyle` | `cardStyle` |  |
| 7 | `repeated Description` | `description` |  |
| 8 | `repeated Relations` | `relations` |  |

#### `Event.Block.Set.Link.CardStyle`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block.Content.Link.CardStyle` | `value` |  |

#### `Event.Block.Set.Link.Description`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block.Content.Link.Description` | `value` |  |

#### `Event.Block.Set.Link.Fields`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Link.IconSize`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.Block.Content.Link.IconSize` | `value` |  |

#### `Event.Block.Set.Link.Relations`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Link.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Link.TargetBlockId`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Relation`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Key` | `key` |  |

#### `Event.Block.Set.Relation.Key`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Restrictions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.Restrictions` | `restrictions` |  |

#### `Event.Block.Set.TableRow`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated IsHeader` | `isHeader` |  |

#### `Event.Block.Set.TableRow.IsHeader`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Text` | `text` |  |
| 3 | `repeated Style` | `style` |  |
| 4 | `repeated Marks` | `marks` |  |
| 5 | `repeated Checked` | `checked` |  |
| 6 | `repeated Color` | `color` |  |
| 7 | `repeated IconEmoji` | `iconEmoji` |  |
| 8 | `repeated IconImage` | `iconImage` |  |

#### `Event.Block.Set.Text.Checked`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text.Color`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text.IconEmoji`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text.IconImage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text.Marks`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text.Style`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Text.Text`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.VerticalAlign`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Block.VerticalAlign` | `verticalAlign` |  |

#### `Event.Block.Set.Widget`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Layout` | `layout` |  |
| 3 | `repeated Limit` | `limit` |  |
| 4 | `repeated ViewId` | `viewId` |  |

#### `Event.Block.Set.Widget.Layout`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Widget.Limit`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Block.Set.Widget.ViewId`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Chat`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Chat.Add`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `orderId` |  |
| 6 | `repeated string` | `afterOrderId` |  |
| 3 | `repeated model.ChatMessage` | `message` |  |
| 4 | `repeated string` | `subIds` |  |
| 5 | `repeated google.protobuf.Struct` | `dependencies` |  |

#### `Event.Chat.Delete`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `subIds` |  |

#### `Event.Chat.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated model.ChatMessage` | `message` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateMentionReadStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |
| 2 | `repeated bool` | `isRead` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateMessageCount`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int32` | `messageCount` |  |
| 2 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateMessageReadStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |
| 2 | `repeated bool` | `isRead` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateMessageSyncStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |
| 2 | `repeated bool` | `isSynced` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdatePinnedStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated model.ChatMessage` | `message` |  |
| 2 | `repeated bool` | `isPinned` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateReactionReadStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |
| 2 | `repeated bool` | `isUnread` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateReactions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated model.ChatMessage.Reactions` | `reactions` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Chat.UpdateState`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated model.ChatState` | `state` |  |
| 2 | `repeated string` | `subIds` |  |

#### `Event.Debug`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Debug.ProfileCreated`

> ProfileCreated is emitted whenever the middleware writes a snapshot archive on its own (e.g. the memory-growth detector), so clients can surface it or queue the archive for upload without polling the profiles directory. Archives produced as a result of a client RPC (DebugRunProfiler) are NOT re-announced via this event — the RPC response already carries the path.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `reason` | reason is a short, stable, UPPER_SNAKE_CASE label describing why the middleware produced this report. It is NOT the DebugRunProfiler Reason enum — values come from the internal call sites: - "MEMORY_GROWTH"  : the desktop memory-growth detector tripped - "LONG_RPC"       : an RPC exceeded the long-execution threshold - "DB_CORRUPTION"  : an anystore/spacestore database failed to open More reasons may be added over time; clients should forward unknown values to Sentry as-is. |
| 2 | `repeated string` | `jsonInfo` | jsonInfo is JSON-encoded context produced by the middleware (reason- specific keys like "sysMemory", "method", "durationMs", "db", "code"). Clients forward it verbatim to Sentry as the event context. |
| 3 | `repeated string` | `path` | path is the absolute path to the snapshot archive on disk; empty when the reason is event-only (e.g. DB_CORRUPTION) and no artifact was produced. |
| 4 | `repeated bool` | `full` | full is true when the archive carries a timed CPU profile + trace in addition to heap and goroutines. False for fast snapshots and for event-only reports. |

#### `Event.File`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.File.LimitReached`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `fileId` |  |

#### `Event.File.LimitUpdated`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.File.LocalUsage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.File.SpaceUsage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `bytesUsage` |  |
| 2 | `repeated string` | `spaceId` |  |

#### `Event.Import`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Import.Finish`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `rootCollectionID` |  |
| 2 | `repeated int64` | `objectsCount` |  |
| 3 | `repeated model.Import.Type` | `importType` |  |

#### `Event.Membership`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Membership.TiersUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Membership.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.MembershipV2`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.MembershipV2.ProductsUpdate`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.MembershipV2.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Message`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 132 | `repeated string` | `spaceId` |  |
| — | (oneof) value | |  |

#### `Event.Notification`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Notification.Send`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Notification.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object.AutoArchive`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `objectIds` |  |

#### `Event.Object.AutoRestore`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `objectIds` |  |

#### `Event.Object.CleanupSuggestion`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `objectIds` | orphan ids (objects at any level + files at level >= 2) created within contextId |
| 2 | `repeated string` | `contextId` | the object that was archived / deleted / had a link removed |
| 3 | `repeated Trigger` | `trigger` |  |

#### `Event.Object.Close`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object.Details`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object.Details.Amend`

> Amend (i.e. add a new key-value pair or update an existing key-value pair) existing state

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated KeyValue` | `details` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Object.Details.Amend.KeyValue`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| 2 | `repeated google.protobuf.Value` | `value` |  |

#### `Event.Object.Details.Set`

> Overwrite current state

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 3 | `repeated string` | `subIds` | state |

#### `Event.Object.Details.Unset`

> Unset existing detail keys

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `keys` |  |
| 3 | `repeated string` | `subIds` |  |

#### `Event.Object.Relations`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object.Relations.Amend`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.RelationLink` | `relationLinks` |  |

#### `Event.Object.Relations.Remove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `relationKeys` |  |

#### `Event.Object.Remove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` | notifies that objects were removed |

#### `Event.Object.Restrictions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object.Restrictions.Set`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated anytype.model.Restrictions` | `restrictions` |  |

#### `Event.Object.Subscription`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Object.Subscription.Add`

> Adds new document to subscriptions

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `afterId` |  |
| 3 | `repeated string` | `subId` |  |

#### `Event.Object.Subscription.Counters`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int64` | `total` | total available records |
| 2 | `repeated int64` | `nextCount` | how many records available after |
| 3 | `repeated int64` | `prevCount` | how many records available before |
| 4 | `repeated string` | `subId` |  |

#### `Event.Object.Subscription.Groups`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `subId` |  |
| 2 | `repeated anytype.model.Block.Content.Dataview.Group` | `group` |  |
| 3 | `repeated bool` | `remove` |  |

#### `Event.Object.Subscription.Position`

> Indicates new position of document

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `afterId` |  |
| 3 | `repeated string` | `subId` |  |

#### `Event.Object.Subscription.Remove`

> Removes document from subscription

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `subId` |  |

#### `Event.P2PStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.P2PStatus.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated Status` | `status` |  |
| 3 | `repeated int64` | `devicesCounter` |  |

#### `Event.Payload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Payload.Broadcast`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Ping`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Process`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Process.Done`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Process.New`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Process.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Space`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Space.SyncStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Space.SyncStatus.Update`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Status` | `status` |  |
| 3 | `repeated Network` | `network` |  |
| 4 | `repeated SyncError` | `error` |  |
| 5 | `repeated int64` | `syncingObjectsCounter` |  |
| 6 | `repeated int64` | `notSyncedFilesCounter` |  |
| 7 | `repeated int64` | `uploadingFilesCounter` |  |

#### `Event.Status`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.Status.Thread`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Summary` | `summary` |  |
| 2 | `repeated Cafe` | `cafe` |  |
| 3 | `repeated Account` | `accounts` |  |

#### `Event.Status.Thread.Account`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated string` | `imageHash` |  |
| 4 | `repeated bool` | `online` |  |
| 5 | `repeated int64` | `lastPulled` |  |
| 6 | `repeated int64` | `lastEdited` |  |
| 7 | `repeated Device` | `devices` |  |

#### `Event.Status.Thread.Cafe`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SyncStatus` | `status` |  |
| 2 | `repeated int64` | `lastPulled` |  |
| 3 | `repeated bool` | `lastPushSucceed` |  |
| 4 | `repeated PinStatus` | `files` |  |

#### `Event.Status.Thread.Cafe.PinStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int32` | `pinning` |  |
| 2 | `repeated int32` | `pinned` |  |
| 3 | `repeated int32` | `failed` |  |
| 4 | `repeated int64` | `updated` |  |

#### `Event.Status.Thread.Device`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `name` |  |
| 2 | `repeated bool` | `online` |  |
| 3 | `repeated int64` | `lastPulled` |  |
| 4 | `repeated int64` | `lastEdited` |  |

#### `Event.Status.Thread.Summary`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.User`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.User.Block`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Event.User.Block.Join`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Account` | `account` |  |

#### `Event.User.Block.Left`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Account` | `account` |  |

#### `Event.User.Block.SelectRange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Account` | `account` |  |
| 2 | `repeated string` | `blockIdsArray` |  |

#### `Event.User.Block.TextRange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Account` | `account` |  |
| 2 | `repeated string` | `blockId` |  |
| 3 | `repeated anytype.model.Range` | `range` |  |

#### `Model`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Model.Process`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 3 | `repeated State` | `state` |  |
| 4 | `repeated Progress` | `progress` |  |
| 5 | `repeated string` | `spaceId` |  |
| — | (oneof) message | |  |
| 11 | `repeated string` | `error` |  |

#### `Model.Process.DropFiles`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Model.Process.Export`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Model.Process.Import`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Model.Process.Migration`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Model.Process.PreloadFile`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Model.Process.Progress`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int64` | `total` |  |
| 2 | `repeated int64` | `done` |  |
| 3 | `repeated string` | `message` |  |

#### `Model.Process.SaveFile`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `ResponseEvent`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Event.Message` | `messages` |  |
| 2 | `repeated string` | `contextId` |  |
| 4 | `repeated string` | `traceId` |  |


### any-block/format/v1/proto/models.proto

#### `Account`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 4 | `repeated Config` | `config` |  |
| 5 | `repeated Status` | `status` |  |
| 6 | `repeated Info` | `info` |  |

#### `Account.Auth`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Account.Auth.AppInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `appHash` |  |
| 2 | `repeated string` | `appName` |  |
| 4 | `repeated string` | `appKey` |  |
| 5 | `repeated int64` | `createdAt` |  |
| 6 | `repeated int64` | `expireAt` |  |
| 7 | `repeated LocalApiScope` | `scope` |  |
| 8 | `repeated bool` | `isActive` |  |

#### `Account.Config`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `enableDataview` |  |
| 2 | `repeated bool` | `enableDebug` |  |
| 3 | `repeated bool` | `enablePrereleaseChannel` |  |
| 4 | `repeated bool` | `enableSpaces` |  |
| 100 | `repeated google.protobuf.Struct` | `extra` |  |

#### `Account.Info`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 2 | `repeated string` | `homeObjectId` |  |
| 3 | `repeated string` | `archiveObjectId` |  |
| 4 | `repeated string` | `profileObjectId` |  |
| 11 | `repeated string` | `marketplaceWorkspaceId` |  |
| 15 | `repeated string` | `workspaceObjectId` |  |
| 16 | `repeated string` | `spaceChatId` |  |
| 8 | `repeated string` | `deviceId` |  |
| 9 | `repeated string` | `accountSpaceId` |  |
| 10 | `repeated string` | `widgetsId` |  |
| 13 | `repeated string` | `spaceViewId` |  |
| 14 | `repeated string` | `techSpaceId` |  |
| 101 | `repeated string` | `gatewayUrl` |  |
| 103 | `repeated string` | `localStoragePath` |  |
| 104 | `repeated string` | `timeZone` |  |
| 105 | `repeated string` | `analyticsId` |  |
| 106 | `repeated string` | `networkId` |  |
| 107 | `repeated string` | `ethereumAddress` |  |
| 108 | `repeated string` | `metaDataKey` |  |

#### `Account.Status`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated StatusType` | `statusType` |  |
| 2 | `repeated int64` | `deletionDate` |  |

#### `Block`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `fields` |  |
| 3 | `repeated Restrictions` | `restrictions` |  |
| 4 | `repeated string` | `childrenIds` |  |
| 5 | `repeated string` | `backgroundColor` |  |
| 6 | `repeated Align` | `align` |  |
| 7 | `repeated VerticalAlign` | `verticalAlign` |  |
| — | (oneof) content | |  |

#### `Block.Content`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.Bookmark`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated string` | `title` | Deprecated. Get this data from the target object. |
| 3 | `repeated string` | `description` | Deprecated. Get this data from the target object. |
| 4 | `repeated string` | `imageHash` | Deprecated. Get this data from the target object. |
| 5 | `repeated string` | `faviconHash` | Deprecated. Get this data from the target object. |
| 6 | `repeated LinkPreview.Type` | `type` |  |
| 7 | `repeated string` | `targetObjectId` |  |
| 8 | `repeated State` | `state` |  |

#### `Block.Content.Chat`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.Dataview`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `source` |  |
| 2 | `repeated View` | `views` |  |
| 3 | `repeated string` | `activeView` |  |
| 4 | `repeated model.Relation` | `relations` | deprecated |
| 12 | `repeated GroupOrder` | `groupOrders` |  |
| 13 | `repeated ObjectOrder` | `objectOrders` |  |
| 5 | `repeated anytype.model.RelationLink` | `relationLinks` |  |
| 6 | `repeated string` | `TargetObjectId` |  |
| 14 | `repeated bool` | `isCollection` |  |

#### `Block.Content.Dataview.Checkbox`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `checked` |  |

#### `Block.Content.Dataview.Date`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.Dataview.Filter`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 9 | `repeated string` | `id` |  |
| 1 | `repeated Operator` | `operator` |  |
| 2 | `repeated string` | `RelationKey` |  |
| 5 | `repeated string` | `relationProperty` |  |
| 3 | `repeated Condition` | `condition` |  |
| 4 | `repeated google.protobuf.Value` | `value` |  |
| 6 | `repeated QuickOption` | `quickOption` |  |
| 7 | `repeated RelationFormat` | `format` |  |
| 8 | `repeated bool` | `includeTime` |  |
| 10 | `repeated Filter` | `nestedFilters` |  |

#### `Block.Content.Dataview.Group`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| — | (oneof) Value | |  |

#### `Block.Content.Dataview.GroupOrder`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `viewId` |  |
| 2 | `repeated ViewGroup` | `viewGroups` |  |

#### `Block.Content.Dataview.ObjectOrder`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `viewId` |  |
| 2 | `repeated string` | `groupId` |  |
| 3 | `repeated string` | `objectIds` |  |

#### `Block.Content.Dataview.Relation`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| 2 | `repeated bool` | `isVisible` |  |
| 3 | `repeated int32` | `width` |  |
| 5 | `repeated bool` | `dateIncludeTime` | bool isReadOnly = 4; // deprecated |
| 6 | `repeated TimeFormat` | `timeFormat` |  |
| 7 | `repeated DateFormat` | `dateFormat` |  |
| 8 | `repeated FormulaType` | `formula` |  |
| 9 | `repeated Block.Align` | `align` |  |

#### `Block.Content.Dataview.Sort`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `RelationKey` |  |
| 2 | `repeated Type` | `type` |  |
| 3 | `repeated google.protobuf.Value` | `customOrder` |  |
| 4 | `repeated RelationFormat` | `format` |  |
| 5 | `repeated bool` | `includeTime` |  |
| 6 | `repeated string` | `id` |  |
| 7 | `repeated EmptyType` | `emptyPlacement` |  |
| 8 | `repeated bool` | `noCollate` |  |

#### `Block.Content.Dataview.Status`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |

#### `Block.Content.Dataview.Tag`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |

#### `Block.Content.Dataview.View`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated Type` | `type` |  |
| 3 | `repeated string` | `name` |  |
| 4 | `repeated Sort` | `sorts` |  |
| 5 | `repeated Filter` | `filters` |  |
| 6 | `repeated Relation` | `relations` |  |
| 7 | `repeated string` | `coverRelationKey` |  |
| 8 | `repeated bool` | `hideIcon` |  |
| 9 | `repeated Size` | `cardSize` |  |
| 10 | `repeated bool` | `coverFit` |  |
| 11 | `repeated string` | `groupRelationKey` |  |
| 12 | `repeated bool` | `groupBackgroundColors` |  |
| 13 | `repeated int32` | `pageLimit` |  |
| 14 | `repeated string` | `defaultTemplateId` |  |
| 15 | `repeated string` | `defaultObjectTypeId` |  |
| 16 | `repeated string` | `endRelationKey` |  |
| 17 | `repeated bool` | `wrapContent` |  |
| 18 | `repeated ListSize` | `listSize` |  |
| 19 | `repeated bool` | `alternateRows` |  |

#### `Block.Content.Dataview.ViewGroup`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `groupId` |  |
| 2 | `repeated int32` | `index` |  |
| 3 | `repeated bool` | `hidden` |  |
| 4 | `repeated string` | `backgroundColor` |  |

#### `Block.Content.Div`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Style` | `style` |  |

#### `Block.Content.FeaturedRelations`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.File`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `hash` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated Type` | `type` |  |
| 4 | `repeated string` | `mime` |  |
| 5 | `repeated int64` | `size` |  |
| 6 | `repeated int64` | `addedAt` |  |
| 9 | `repeated string` | `targetObjectId` |  |
| 7 | `repeated State` | `state` |  |
| 8 | `repeated Style` | `style` |  |

#### `Block.Content.Icon`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `name` |  |

#### `Block.Content.Latex`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `text` |  |
| 2 | `repeated Processor` | `processor` |  |

#### `Block.Content.Layout`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Style` | `style` |  |

#### `Block.Content.Link`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `targetBlockId` |  |
| 2 | `repeated Style` | `style` |  |
| 3 | `repeated google.protobuf.Struct` | `fields` |  |
| 4 | `repeated IconSize` | `iconSize` |  |
| 5 | `repeated CardStyle` | `cardStyle` |  |
| 6 | `repeated Description` | `description` |  |
| 7 | `repeated string` | `relations` |  |

#### `Block.Content.Relation`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |

#### `Block.Content.Smartblock`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.Table`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.TableColumn`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.TableOfContents`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Block.Content.TableRow`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `isHeader` |  |

#### `Block.Content.Text`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `text` |  |
| 2 | `repeated Style` | `style` |  |
| 3 | `repeated Marks` | `marks` |  |
| 4 | `repeated bool` | `checked` |  |
| 5 | `repeated string` | `color` |  |
| 6 | `repeated string` | `iconEmoji` |  |
| 7 | `repeated string` | `iconImage` |  |

#### `Block.Content.Text.Mark`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Range` | `range` |  |
| 2 | `repeated Type` | `type` |  |
| 3 | `repeated string` | `param` |  |

#### `Block.Content.Text.Marks`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Mark` | `marks` |  |

#### `Block.Content.Widget`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Layout` | `layout` |  |
| 2 | `repeated int32` | `limit` |  |
| 3 | `repeated string` | `viewId` |  |
| 4 | `repeated bool` | `autoAdded` |  |

#### `Block.Restrictions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `read` |  |
| 2 | `repeated bool` | `edit` |  |
| 3 | `repeated bool` | `remove` |  |
| 4 | `repeated bool` | `drag` |  |
| 5 | `repeated bool` | `dropOn` |  |

#### `BlockMetaOnly`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `fields` |  |

#### `ChatMessage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `orderId` |  |
| 3 | `repeated string` | `creator` |  |
| 4 | `repeated int64` | `createdAt` |  |
| 9 | `repeated int64` | `modifiedAt` |  |
| 11 | `repeated string` | `stateId` | stateId is ever-increasing id (BSON ObjectId) for this message. Unlike orderId, this ID is ordered by the time messages are added. For example, it's useful to prevent accidental reading of messages from the past when a ChatReadMessages request is sent: a message from the past may appear, but the client is still unaware of it |
| 5 | `repeated string` | `replyToMessageId` |  |
| 6 | `repeated MessageContent` | `message` |  |
| 7 | `repeated Attachment` | `attachments` |  |
| 8 | `repeated Reactions` | `reactions` |  |
| 10 | `repeated bool` | `read` |  |
| 12 | `repeated bool` | `mentionRead` |  |
| 14 | `repeated bool` | `hasMention` |  |
| 13 | `repeated bool` | `synced` |  |
| 15 | `repeated bool` | `pinned` |  |
| 16 | `repeated bool` | `unreadReaction` |  |
| 17 | `repeated MessageBlock` | `blocks` |  |

#### `ChatMessage.Attachment`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `target` |  |
| 2 | `repeated AttachmentType` | `type` |  |

#### `ChatMessage.MessageBlock`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) content | |  |

#### `ChatMessage.MessageBlockEditorQuote`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `blockId` |  |
| 2 | `repeated MessageBlockText` | `content` |  |

#### `ChatMessage.MessageBlockEmbed`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `text` |  |
| 2 | `repeated Block.Content.Latex.Processor` | `processor` |  |

#### `ChatMessage.MessageBlockLink`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `targetObjectId` |  |
| 2 | `repeated LinkType` | `type` |  |

#### `ChatMessage.MessageBlockMessageQuote`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `messageId` |  |
| 2 | `repeated string` | `participantId` |  |
| 3 | `repeated MessageBlockText` | `content` |  |

#### `ChatMessage.MessageBlockText`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `text` |  |
| 2 | `repeated Block.Content.Text.Style` | `style` |  |
| 3 | `repeated Block.Content.Text.Mark` | `marks` |  |
| 4 | `repeated bool` | `checked` |  |
| 5 | `repeated string` | `lang` |  |

#### `ChatMessage.MessageContent`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `text` |  |
| 2 | `repeated Block.Content.Text.Style` | `style` |  |
| 3 | `repeated Block.Content.Text.Mark` | `marks` |  |

#### `ChatMessage.Reactions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated map<string, IdentityList>` | `reactions` |  |

#### `ChatMessage.Reactions.IdentityList`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ids` |  |

#### `ChatState`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated UnreadState` | `messages` |  |
| 2 | `repeated UnreadState` | `mentions` |  |
| 3 | `repeated string` | `lastStateId` |  |
| 4 | `repeated int64` | `order` |  |
| 5 | `repeated string` | `unreadReactionOrderId` |  |

#### `ChatState.UnreadState`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `oldestOrderId` |  |
| 2 | `repeated int32` | `counter` |  |

#### `Detail`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| 2 | `repeated google.protobuf.Value` | `value` |  |

#### `DeviceInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated int64` | `addDate` |  |
| 4 | `repeated bool` | `archived` |  |
| 5 | `repeated bool` | `isConnected` |  |

#### `Export`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `FileEncryptionKey`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `path` |  |
| 2 | `repeated string` | `key` |  |

#### `FileInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fileId` |  |
| 2 | `repeated FileEncryptionKey` | `encryptionKeys` |  |

#### `IdentityProfile`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated string` | `iconCid` |  |
| 4 | `repeated FileEncryptionKey` | `iconEncryptionKeys` |  |
| 5 | `repeated string` | `description` |  |
| 6 | `repeated string` | `globalName` |  |

#### `IdentityProfileWithKey`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated IdentityProfile` | `identityProfile` |  |
| 2 | `repeated bytes` | `requestMetadata` |  |

#### `Import`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `InternalFlag`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Value` | `value` |  |

#### `Invite`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` |  |
| 2 | `repeated bytes` | `signature` |  |

#### `InvitePayload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `creatorIdentity` |  |
| 2 | `repeated string` | `creatorName` |  |
| 12 | `repeated string` | `creatorIconCid` |  |
| 13 | `repeated FileEncryptionKey` | `creatorIconEncryptionKeys` |  |
| 3 | `repeated bytes` | `aclKey` |  |
| 4 | `repeated string` | `spaceId` |  |
| 5 | `repeated string` | `spaceName` |  |
| 6 | `repeated string` | `spaceIconCid` |  |
| 10 | `repeated uint32` | `spaceIconOption` |  |
| 11 | `repeated uint32` | `spaceUxType` |  |
| 14 | `repeated uint32` | `spaceType` |  |
| 7 | `repeated FileEncryptionKey` | `spaceIconEncryptionKeys` |  |
| 8 | `repeated InviteType` | `inviteType` |  |
| 9 | `repeated bytes` | `guestKey` |  |

#### `Layout`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated ObjectType.Layout` | `id` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated Relation` | `requiredRelations` |  |

#### `LinkPreview`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated string` | `title` |  |
| 3 | `repeated string` | `description` |  |
| 4 | `repeated string` | `imageUrl` |  |
| 5 | `repeated string` | `faviconUrl` |  |
| 6 | `repeated Type` | `type` |  |

#### `ManifestInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 2 | `repeated string` | `id` |  |
| 3 | `repeated string` | `name` |  |
| 4 | `repeated string` | `author` |  |
| 5 | `repeated string` | `license` |  |
| 6 | `repeated string` | `title` |  |
| 7 | `repeated string` | `description` |  |
| 8 | `repeated string` | `screenshots` |  |
| 9 | `repeated string` | `downloadLink` |  |
| 10 | `repeated int32` | `fileSize` |  |
| 11 | `repeated string` | `categories` |  |
| 12 | `repeated string` | `language` |  |

#### `Membership`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `tier` | it was Tier before, changed to int32 to allow dynamic values |
| 2 | `repeated Status` | `status` |  |
| 3 | `repeated uint64` | `dateStarted` |  |
| 4 | `repeated uint64` | `dateEnds` |  |
| 5 | `repeated bool` | `isAutoRenew` |  |
| 6 | `repeated PaymentMethod` | `paymentMethod` |  |
| 7 | `repeated string` | `nsName` | can be empty if user did not ask for any name |
| 8 | `repeated anytype.model.NameserviceNameType` | `nsNameType` |  |
| 9 | `repeated string` | `userEmail` | if the email was verified by the user or set during the checkout - it will be here |
| 10 | `repeated bool` | `subscribeToNewsletter` |  |

#### `MembershipTierData`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `id` | this is a unique Payment Node ID of the tier WARNING: tiers can be sorted differently, not according to their IDs! |
| 2 | `repeated string` | `name` | localazied name of the tier |
| 3 | `repeated string` | `description` | just a short technical description |
| 4 | `repeated bool` | `isTest` | is this tier for testing and debugging only? |
| 5 | `repeated PeriodType` | `periodType` | how long is the period of the subscription |
| 6 | `repeated uint32` | `periodValue` | i.e. "5 days" or "3 years" |
| 7 | `repeated uint32` | `priceStripeUsdCents` | this one is a price we use ONLY on Stripe platform |
| 8 | `repeated uint32` | `anyNamesCountIncluded` | number of ANY NS names that this tier includes also in the "features" list (see below) |
| 9 | `repeated uint32` | `anyNameMinLength` | somename.any - is of len 8 |
| 10 | `repeated string` | `features` | localized strings for the features |
| 11 | `repeated string` | `colorStr` | green, blue, red, purple, custom |
| 12 | `repeated string` | `stripeProductId` | Stripe platform-specific data: |
| 13 | `repeated string` | `stripeManageUrl` |  |
| 15 | `repeated string` | `iosProductId` | iOS platform-specific data: |
| 16 | `repeated string` | `iosManageUrl` |  |
| 17 | `repeated string` | `androidProductId` | Android platform-specific data: |
| 18 | `repeated string` | `androidManageUrl` |  |
| 19 | `repeated string` | `offer` | "limited offer" or somehing like that |

#### `MembershipV2`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.Amount`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `currency` | ISO 4217 currency code |
| 2 | `repeated int64` | `amountCents` | $0.01 = 1 $1.00 = 100 also supports negative amounts! some invoices can have negatice amount (refund) |

#### `MembershipV2.Cart`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated CartProduct` | `products` | if you add Nx the same product - it will be Nx in the 'products' array, i.e: each product instance has a unique index |
| 2 | `repeated Amount` | `total` | total amount of the cart (including discounts, etc) |
| 3 | `repeated Amount` | `totalNextInvoice` | in case you are paying in the middle of the period (for existing customers) the next invoice amount will also be generated |
| 4 | `repeated uint64` | `nextInvoiceDate` |  |
| 5 | `repeated string` | `appliedPromocodes` |  |

#### `MembershipV2.CartProduct`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Product` | `product` |  |
| 2 | `repeated bool` | `isYearly` | otherwise - monthly or isLifetime |
| 3 | `repeated bool` | `remove` | set to true if you want to remove this item from the customer it's like setting -1 to some product |
| 4 | `repeated bool` | `isLifetime` | if true - then this is lifetime product (no matter what isYearly above is) unfortunately we do not use Period here to keep compatibility with old versions that still use isYearly! |

#### `MembershipV2.CryptoCheckout`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `invoiceURL` |  |
| 2 | `repeated Amount` | `total` |  |
| 3 | `repeated bool` | `isCanCancel` |  |

#### `MembershipV2.Data`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated PurchasedProduct` | `products` |  |
| 2 | `repeated Invoice` | `nextInvoice` |  |
| 3 | `repeated string` | `teamOwnerID` |  |
| 4 | `repeated PaymentProvider` | `paymentProvider` |  |
| 5 | `repeated string` | `appliedPromocodes` |  |

#### `MembershipV2.Features`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `storageBytes` |  |
| 2 | `repeated uint32` | `spaceReaders` |  |
| 3 | `repeated uint32` | `spaceWriters` |  |
| 4 | `repeated uint32` | `sharedSpaces` |  |
| 5 | `repeated uint32` | `teamSeats` |  |
| 6 | `repeated uint32` | `anyNameCount` |  |
| 7 | `repeated uint32` | `anyNameMinLen` |  |
| 8 | `repeated uint32` | `privateSpaces` |  |

#### `MembershipV2.Invoice`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `date` |  |
| 2 | `repeated Amount` | `total` |  |

#### `MembershipV2.Product`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated string` | `description` |  |
| 4 | `repeated bool` | `isTopLevel` |  |
| 5 | `repeated bool` | `isHidden` |  |
| 6 | `repeated bool` | `isIntro` | isIntro flag can be used as follows:  1. if current user's top level product has isIntro flag -> then you'd rather show a FULL list of all products to enable upgrading from CURRENT product 2. but if current user's top level product has no isIntro flag -> then it means that this plan was aquired and user need to control it. then show "second screen" to control that product instead |
| 7 | `repeated bool` | `isUpgradeable` | isUpgradeable can be used as follows:  if current user's top level product has isUpgradeable flag -> show incentives to buy something else |
| 8 | `repeated Amount` | `pricesYearly` |  |
| 9 | `repeated Amount` | `pricesMonthly` |  |
| 10 | `repeated string` | `colorStr` | green, blue, red, purple, custom, etc |
| 11 | `repeated string` | `offer` |  |
| 12 | `repeated Features` | `features` |  |
| 13 | `repeated Amount` | `pricesLifetime` |  |

#### `MembershipV2.ProductStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Status` | `status` |  |

#### `MembershipV2.PurchaseInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `dateStarted` |  |
| 2 | `repeated uint64` | `dateEnds` |  |
| 3 | `repeated bool` | `isAutoRenew` |  |
| 4 | `repeated Period` | `period` |  |

#### `MembershipV2.PurchasedProduct`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Product` | `product` |  |
| 2 | `repeated PurchaseInfo` | `purchaseInfo` |  |
| 3 | `repeated ProductStatus` | `productStatus` |  |

#### `Metadata`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) payload | |  |

#### `Metadata.Payload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Metadata.Payload.IdentityPayload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `profileSymKey` |  |

#### `Notification`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated int64` | `createTime` |  |
| 4 | `repeated Status` | `status` |  |
| 5 | `repeated bool` | `isLocal` |  |
| — | (oneof) payload | |  |
| 7 | `repeated string` | `space` |  |
| 14 | `repeated string` | `aclHeadId` |  |

#### `Notification.Export`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 2 | `repeated Code` | `errorCode` |  |
| 3 | `repeated model.Export.Format` | `exportType` |  |

#### `Notification.GalleryImport`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `processId` |  |
| 2 | `repeated model.Import.ErrorCode` | `errorCode` |  |
| 3 | `repeated string` | `spaceId` |  |
| 4 | `repeated string` | `name` |  |
| 5 | `repeated string` | `spaceName` |  |

#### `Notification.Import`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `processId` |  |
| 2 | `repeated model.Import.ErrorCode` | `errorCode` |  |
| 3 | `repeated model.Import.Type` | `importType` |  |
| 4 | `repeated string` | `spaceId` |  |
| 5 | `repeated string` | `name` |  |
| 6 | `repeated string` | `spaceName` |  |

#### `Notification.ParticipantPermissionsChange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated ParticipantPermissions` | `permissions` |  |
| 3 | `repeated string` | `spaceName` |  |

#### `Notification.ParticipantRemove`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` |  |
| 2 | `repeated string` | `identityName` |  |
| 3 | `repeated string` | `identityIcon` |  |
| 4 | `repeated string` | `spaceId` |  |
| 5 | `repeated string` | `spaceName` |  |

#### `Notification.ParticipantRequestApproved`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated ParticipantPermissions` | `permissions` |  |
| 5 | `repeated string` | `spaceName` |  |

#### `Notification.ParticipantRequestDecline`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 3 | `repeated string` | `spaceName` |  |

#### `Notification.RequestToJoin`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `identity` |  |
| 3 | `repeated string` | `identityName` |  |
| 4 | `repeated string` | `identityIcon` |  |
| 5 | `repeated string` | `spaceName` |  |

#### `Notification.RequestToLeave`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `identity` |  |
| 3 | `repeated string` | `identityName` |  |
| 4 | `repeated string` | `identityIcon` |  |
| 5 | `repeated string` | `spaceName` |  |

#### `Notification.Test`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Object`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Object.ChangePayload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SmartBlockType` | `smartBlockType` |  |
| 2 | `repeated string` | `key` |  |
| 3 | `repeated bytes` | `data` |  |

#### `ObjectType`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated RelationLink` | `relationLinks` |  |
| 4 | `repeated Layout` | `layout` |  |
| 5 | `repeated string` | `iconEmoji` |  |
| 6 | `repeated string` | `description` |  |
| 7 | `repeated bool` | `hidden` |  |
| 10 | `repeated bool` | `readonly` |  |
| 8 | `repeated SmartBlockType` | `types` |  |
| 9 | `repeated bool` | `isArchived` |  |
| 11 | `repeated bool` | `installedByDefault` |  |
| 12 | `repeated string` | `key` |  |
| 13 | `repeated int64` | `revision` |  |
| 14 | `repeated bool` | `restrictObjectCreation` |  |
| 15 | `repeated int64` | `iconColor` |  |
| 16 | `repeated string` | `iconName` |  |
| 17 | `repeated string` | `pluralName` |  |

#### `ObjectView`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `rootId` |  |
| 2 | `repeated Block` | `blocks` |  |
| 3 | `repeated DetailsSet` | `details` |  |
| 4 | `repeated SmartBlockType` | `type` |  |
| 7 | `repeated Relation` | `relations` |  |
| 10 | `repeated RelationLink` | `relationLinks` |  |
| 8 | `repeated Restrictions` | `restrictions` |  |
| 9 | `repeated HistorySize` | `history` |  |
| 11 | `repeated BlockParticipant` | `blockParticipants` |  |

#### `ObjectView.BlockParticipant`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `blockId` |  |
| 2 | `repeated string` | `participantId` |  |

#### `ObjectView.DetailsSet`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated google.protobuf.Struct` | `details` |  |
| 3 | `repeated string` | `subIds` |  |

#### `ObjectView.HistorySize`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int32` | `undo` |  |
| 2 | `repeated int32` | `redo` |  |

#### `ObjectView.RelationWithValuePerObject`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `objectId` |  |
| 2 | `repeated RelationWithValue` | `relations` |  |

#### `ParticipantPermissionChange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` |  |
| 2 | `repeated ParticipantPermissions` | `perms` |  |

#### `Placeholder`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `relationKey` |  |
| 2 | `repeated Value` | `values` |  |

#### `Placeholder.Value`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Type` | `type` |  |
| 2 | `repeated google.protobuf.Value` | `value` |  |

#### `Range`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int32` | `from` |  |
| 2 | `repeated int32` | `to` |  |

#### `Relation`

> Relation describe the human-interpreted relation type. It may be something like "Date of creation, format=date" or "Assignee, format=objectId, objectType=person"

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 100 | `repeated string` | `id` |  |
| 1 | `repeated string` | `key` | Key under which the value is stored in the map. Must be unique for the object type. It usually auto-generated bsonid, but also may be something human-readable in case of prebuilt types. |
| 2 | `repeated RelationFormat` | `format` |  |
| 3 | `repeated string` | `name` |  |
| 4 | `repeated google.protobuf.Value` | `defaultValue` |  |
| 5 | `repeated DataSource` | `dataSource` |  |
| 6 | `repeated bool` | `hidden` |  |
| 7 | `repeated bool` | `readOnly` |  |
| 15 | `repeated bool` | `readOnlyRelation` |  |
| 8 | `repeated bool` | `multi` |  |
| 9 | `repeated string` | `objectTypes` |  |
| 12 | `repeated Option` | `selectDict` | index 10, 11 was used in internal-only builds. Can be reused, but may break some test accounts |
| 13 | `repeated int32` | `maxCount` |  |
| 14 | `repeated string` | `description` |  |
| 20 | `repeated Scope` | `scope` | on-store fields, injected only locally |
| 21 | `repeated string` | `creator` |  |
| 22 | `repeated int64` | `revision` |  |
| 23 | `repeated bool` | `includeTime` |  |

#### `Relation.Option`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `text` |  |
| 3 | `repeated string` | `color` |  |
| 5 | `repeated string` | `relationKey` | 4 is reserved for old relation format |
| 6 | `repeated string` | `orderId` |  |

#### `RelationLink`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| 2 | `repeated RelationFormat` | `format` |  |

#### `RelationOptions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Relation.Option` | `options` |  |

#### `RelationWithValue`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Relation` | `relation` |  |
| 2 | `repeated google.protobuf.Value` | `value` |  |

#### `Relations`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Relation` | `relations` |  |

#### `Restrictions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated ObjectRestriction` | `object` |  |
| 2 | `repeated DataviewRestrictions` | `dataview` |  |

#### `Restrictions.DataviewRestrictions`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `blockId` |  |
| 2 | `repeated DataviewRestriction` | `restrictions` |  |

#### `Search`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Search.Message`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `Search.Message.Result`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `chatId` |  |
| 2 | `repeated string` | `messageId` |  |
| 3 | `repeated int64` | `score` |  |
| 4 | `repeated string` | `highlight` |  |
| 5 | `repeated Range` | `highlightRanges` |  |
| 6 | `repeated ChatMessage` | `message` |  |
| 7 | `repeated string` | `spaceId` |  |

#### `Search.Message.Sort`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Key` | `key` |  |
| 2 | `repeated Type` | `type` |  |

#### `Search.Meta`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `highlight` |  |
| 2 | `repeated Range` | `highlightRanges` |  |
| 3 | `repeated string` | `blockId` |  |
| 4 | `repeated string` | `relationKey` |  |
| 5 | `repeated google.protobuf.Struct` | `relationDetails` |  |

#### `Search.Result`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `objectId` |  |
| 2 | `repeated google.protobuf.Struct` | `details` |  |
| 3 | `repeated Meta` | `meta` |  |

#### `SmartBlockSnapshotBase`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Block` | `blocks` |  |
| 2 | `repeated google.protobuf.Struct` | `details` |  |
| 5 | `repeated string` | `objectTypes` |  |
| 6 | `repeated google.protobuf.Struct` | `collections` |  |
| 8 | `repeated string` | `removedCollectionKeys` |  |
| 7 | `repeated RelationLink` | `relationLinks` |  |
| 9 | `repeated string` | `key` |  |
| 10 | `repeated int64` | `originalCreatedTimestamp` |  |
| 11 | `repeated FileInfo` | `fileInfo` |  |

#### `SpaceObjectHeader`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceID` |  |


