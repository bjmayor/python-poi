# env

Python 3.12.2

# 说明

```sql
CREATE TABLE `group` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) UNIQUE NOT NULL
);
```

# 先查询再创建

## 方案 1 √

如果不存在则插入。需要处理并发插入的情况。重复插入时返回第一次插入的 id。

```sql
insert into `group` (name) values ('group1') ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id);
```

# 说明

发现一个问题。id 有跨度。原因是在并发环境下，重复插入确实会导致自增 ID 增加，即使插入没有产生新记录。
https://www.cnblogs.com/lixuwu/p/15904759.html 参考自增值的修改时机。

根本原因就是先修改的 auto_increment 值，后插入。
当插入失败或者回滚了。auto_increment 值不会改回去。

1. 可以看到，这个表的自增值改成 3，是在真正执行插入数据的操作之前。这个语句真正执行的时候，因为碰到唯一键 c 冲突，所以 id=2 这一行并没有插入成功，但也没有将自增值再改回去。
2. 事务回滚也会产生类似的现象，这就是第二种原因。
