> 本文档为 any-sync 官方文档《Access control and Encryption》（访问控制与加密）的中文汉化版。
> 原文：https://sync.any.org/access-control/（英文为准）｜ 汉化日期：2026-09-16 ｜ 技术术语保留英文原词并附中文释义

# 访问控制与加密（Access Control and Encryption）

## 概述

`any-sync` 使用「频道（Channel，亦称空间 Space）」这一抽象，在多个设备和用户之间同步与共享数据。频道通过**端到端加密**保护，使用由 BIP-39 助记词派生的**用户自有密钥**。这一设计确保变更（Change）被加密签名，支持离线创建频道以及点对点（P2P）同步，无需持续连接任何外部网络或区块链。

当前 P2P 同步基于 mDNS 协议在本地网络运行，未来计划通过中继节点扩展至全球范围。当只有两名参与者协作时，不需要外部共识机制；但若三个或更多用户共享同一频道，就必须维护一份**访问控制列表（ACL）**。任何对 ACL 的修改（如变更权限、添加/移除成员）都由**共识节点（Consensus Node）**验证——共识节点可以是区块链，也可以采用 RAFT 等共识机制。该机制用于处理分布式系统的边界情况，同时保障频道的所有权。

所有数据——无论静态存储还是传输途中——都经过端到端加密，因此同步服务提供商无法读取频道内容。频道独立于任何特定链；只有在修改 ACL 或托管网络拓扑配置时，才需要访问外部网络或区块链。

## 保险库与密码学（Vault & Cryptography）

### 保险库创建（Vault Inception）

用户创建**保险库（Vault）**时，会从一条 BIP-39 助记词（12 个单词）派生出一组密钥。整个过程完全离线完成，私钥始终保留在设备上。派生的密钥如下：

![密钥派生示意（BIP-39 Seed Phrase → Master / Identity / Ethereum / Device Key；Identity → Replication Key 与 Metadata Key）](@./images/key-derivation.png)

| 密钥 | 用途 |
| --- | --- |
| 主密钥（Master Key） | 用于在 ACL 记录中签名/认证身份（Identity），必要时用于恢复身份 |
| 身份密钥（Identity Key） | 作为保险库所有者的公钥，在 ACL 记录中签署空间头（Space headers） |
| 以太坊密钥（Ethereum Key） | 用于签署以太坊交易，供 Any 命名系统（ANS）按需使用 |
| 复制密钥（Replication Key） | 由身份派生，用于同步节点之间的负载均衡与空间分区 |
| 身份元数据密钥（Identity Metadata Key） | 用于加密 ACL 记录中的身份元数据 |
| 对等（设备）密钥（Peer / Device Key） | 用于 P2P 组网与握手的 Ed25519 密钥对 |

每一把密钥在 `any-sync` 密码学框架中承担独特角色，共同管理身份、访问与加密。

### 频道创建（Channel Creation）

用户创建频道时，会使用保险库中的密钥生成一份**ACL 根记录（ACL root record）**。此过程在客户端离线完成；频道内所有对象（Objects）与变更（Changes）都使用 ACL 的密钥加密。由此，创建者在决定共享之前，对频道拥有完整的所有权与控制权。

### 频道共享（Channel Sharing）

向他人共享频道时，客户端生成一条包含新身份公钥的新 ACL 记录。此后，频道内所有对象都使用这条更新的 ACL 记录进行加密。每条新 ACL 记录还会加密前一条记录的密钥，形成一条**加密链**，使授权成员能够解密历史状态。添加/移除成员或调整访问级别时重复此过程。这些操作需要连接共识节点（链上或链下）以验证并最终确认 ACL 更新。

## 原语（Primitives）

| 原语 | 释义 |
| --- | --- |
| 保险库（Vault） | 存储并管理用户密钥集合的本地抽象层 |
| 助记词（Seed Phrase, BIP-39） | 12 个单词，用于派生密钥；BIP-39 标准提供固定 2048 词词典 |
| 主密钥（Master Key） | Ed25519 密钥对（SLIP10），派生路径 `m/44'/code'/index'`，用于认证/恢复身份 |
| 身份密钥（Identity Key） | 另一 Ed25519 密钥对（SLIP10），派生路径 `m/44'/code'/index'/0'`，作为保险库的公钥身份，在 ACL 记录中签署频道头 |
| 设备密钥（Device Key / Peer Key） | 保险库创建时随机生成的 Ed25519 密钥对，作为托管提供商网络中的 Peer ID，管理 P2P 握手（Diffie-Hellman 与 Anytype 握手） |
| 以太坊密钥（Ethereum Key） | ECDSA 密钥对，派生路径 `m/44'/60'/Index'/0/0`，用于 Any 命名系统（ANS）的以太坊交易 |
| 复制密钥（Replication Key） | 由身份派生，用于一致性哈希确定哪些节点同步给定空间 |
| 元数据密钥（Metadata Key） | Ed25519 密钥对，加密 ACL 记录中的身份元数据 |
| 读取密钥（Read Key） | 对称 AES 密钥，授予 ACL 记录的读取权限，用每个授权成员的公钥加密 |
| 频道 ID（Channel Id） | 唯一标识频道的 CID（内容标识符），由身份与复制密钥组合生成，保障频道真实性 |
| 访问控制列表（ACL） | 严格有序的权限记录列表；每个频道一条 ACL，每条记录描述身份的添加/移除、密钥轮换或权限变更 |
| ACL 记录（ACL Record） | ACL 严格有序列表中的不可变条目，引用主密钥、身份密钥、元数据密钥与读取密钥，授予或拒绝频道内对象操作 |
| ACL 根（ACL Root） | 第一条 ACL 记录，在客户端保险库中离线创建，确立频道的基础所有权与加密 |

## ACL 详解（ACLs in Detail）

ACL 是一种**内容寻址（content-addressable）**数据结构，其 ID 与其初始（根）记录的 ID 一致。ACL 构成严格有序的记录列表，最新记录称为「头部（head）」。每条记录可描述：

- 添加新身份
- 修改或移除现有身份
- 更换加密密钥
- 调整权限（如读、写、拥有）

### ACL 与加密

1. **空间、对象与变更的加密**
   - 客户端发起变更（Change），用对象的对称密钥加密。
   - 对象密钥由空间当前对称密钥（由 ACL 管理）与对象 CID 组合派生。
   - 空间对称密钥为每个当前成员分别加密；该密钥还加密所有先前密钥，形成链条，授权成员可解密完整历史。
2. **文件的加密**
   - 每个文件使用自己的对称密钥加密内容。
   - 该密钥存储在「文件对象（File Object）」中，文件对象本身按 ACL 方案加密。
3. **变更的验证**
   - 所有变更由身份密钥签名，确保变更来源可经密码学验证。

![读取密钥轮换示意（Read Key M → M+1，随 ACL 记录 N → N+1 → N+2 移除用户 B、添加用户 C）](@./images/read-key-rotation.png)

### ACL 角色

以下角色定义频道内每个成员的权限级别：

```
enum AclUserPermissions {

    None = 0;

    Owner = 1; // Can invite/remove members, edit Objects, and remove Space from a Subnet

    Admin = 2; // Can invite/remove members, edit Objects

    Writer = 3; // Can add/edit Objects

    Reader = 4; // Can only view Objects

}
```

- **拥有者（Owner）**：完全控制，包括重新配置或从子网移除空间。
- **管理员（Admin）**：可邀请/撤销成员、编辑访问级别、修改对象。
- **写者（Writer）**：可创建和修改对象。
- **读者（Reader）**：只读访问。

### ACL 密钥轮换操作

ACL 记录可包含多种更新密钥与权限的操作：

- 邀请 / 撤销邀请（Invite / Revoke Invite）
- 加入请求 / 接受请求 / 拒绝请求（Request to Join / Accept Request / Decline Request）
- 移除账户 / 移除账户请求（Remove Account / Remove Account Request）
- 变更权限 / 批量变更权限（Change Permission / Change Permissions）
- 更换读取密钥（Change Read Key）
- 批量添加账户（Add Accounts）
- 取消请求（Cancel Request）

以下是展示 ACL 记录结构的示例 protobuf 消息：

```
message AclRoot {

  bytes identity = 1;

  bytes masterKey = 2;

  string spaceId = 3;

  bytes encryptedReadKey = 4;

  int64 timestamp = 5;

  bytes identitySignature = 6;

  bytes metadataPubKey = 7;

  bytes encryptedMetadataPrivKey = 8;

  bytes encryptedOwnerMetadata = 9;

}
```

```
message AclContentValue {

  oneof value {

    AclAccountInvite invite = 1;

    AclAccountInviteRevoke inviteRevoke = 2;

    AclAccountRequestJoin requestJoin = 3;

    AclAccountRequestAccept requestAccept = 4;

    AclAccountPermissionChange permissionChange = 5;

    AclAccountRemove accountRemove = 6;

    AclReadKeyChange readKeyChange = 7;

    AclAccountRequestDecline requestDecline = 8;

    AclAccountRequestRemove accountRequestRemove = 9;

    AclAccountPermissionChanges permissionChanges = 10;

    AclAccountsAdd accountsAdd = 11;

    AclAccountRequestCancel requestCancel = 12;

  }

}
```

## 总结

`any-sync` 的访问控制与加密模型依赖客户端自有密钥（由 BIP-39 助记词生成）。该设计让用户能够完全离线创建、共享和管理频道；多用户协作则借助 ACL，并由共识机制验证，以安全处理复杂的权限逻辑。

- **频道** 在需要 ACL 或其变更之前，始终独立于任何链。
- **基于保险库的密钥管理** 确保每个用户保留其加密资产的所有权。
- **端到端加密** 覆盖所有静态与传输中的数据，保护用户隐私。

该架构在灵活性（支持纯本地或 P2P 部署）与安全性（可选接入更广泛的共识网络或区块链）之间取得平衡。
