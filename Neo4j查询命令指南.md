# Neo4j查询命令指南

## 🌐 访问Neo4j浏览器

1. **打开浏览器访问**：http://localhost:7474
2. **登录信息**：
   - 用户名：`neo4j`
   - 密码：`password`

## 📊 基础查询命令

### 1. 查看数据库统计信息

```cypher
// 查看所有节点数量
MATCH (n) RETURN count(n) as total_nodes

// 查看所有关系数量
MATCH ()-[r]->() RETURN count(r) as total_relationships

// 查看节点类型统计
MATCH (n) RETURN labels(n) as node_type, count(n) as count ORDER BY count DESC
```

### 2. 查看疾病数据

```cypher
// 查看前10个疾病
MATCH (d:Disease) RETURN d.name, d.desc LIMIT 10

// 查看特定疾病
MATCH (d:Disease) WHERE d.name CONTAINS "高血压" RETURN d.name, d.desc

// 查看疾病数量
MATCH (d:Disease) RETURN count(d) as disease_count
```

### 3. 查看症状数据

```cypher
// 查看前10个症状
MATCH (s:Symptom) RETURN s.name LIMIT 10

// 查看症状数量
MATCH (s:Symptom) RETURN count(s) as symptom_count
```

### 4. 查看关系数据

```cypher
// 查看疾病-症状关系
MATCH (d:Disease)-[r:has_symptom]->(s:Symptom) 
RETURN d.name, s.name LIMIT 10

// 查看疾病-药品关系
MATCH (d:Disease)-[r:common_drug]->(drug:Drug) 
RETURN d.name, drug.name LIMIT 10

// 查看疾病-并发症关系
MATCH (d:Disease)-[r:acompany_with]->(comp:Disease) 
RETURN d.name, comp.name LIMIT 10
```

### 5. 查看JSON格式数据

```cypher
// 查看疾病的完整信息（JSON格式）
MATCH (d:Disease) 
RETURN d.name as disease_name, 
       d.desc as description,
       d.cure_department as department,
       d.cure_way as treatment,
       d.cure_lasttime as duration,
       d.symptom as symptoms,
       d.cause as causes,
       d.prevent as prevention,
       d.note as notes,
       d.yibao_status as insurance_status
LIMIT 5
```

### 6. 复杂查询示例

```cypher
// 查询高血压的相关信息
MATCH (d:Disease {name: "高血压"})
OPTIONAL MATCH (d)-[r1:has_symptom]->(s:Symptom)
OPTIONAL MATCH (d)-[r2:common_drug]->(drug:Drug)
OPTIONAL MATCH (d)-[r3:acompany_with]->(comp:Disease)
RETURN d.name as disease_name,
       d.desc as description,
       collect(DISTINCT s.name) as symptoms,
       collect(DISTINCT drug.name) as drugs,
       collect(DISTINCT comp.name) as complications
```

### 7. 可视化查询

```cypher
// 查看疾病关系网络（可视化）
MATCH (d:Disease {name: "高血压"})-[r]-(n)
RETURN d, r, n LIMIT 20

// 查看症状关系网络
MATCH (s:Symptom {name: "头痛"})-[r]-(n)
RETURN s, r, n LIMIT 20
```

## 🔍 高级查询技巧

### 1. 路径查询

```cypher
// 查找从疾病到症状的路径
MATCH path = (d:Disease)-[:has_symptom]->(s:Symptom)
WHERE d.name = "高血压"
RETURN path LIMIT 10

// 查找多跳关系
MATCH path = (d:Disease)-[:has_symptom]->(s:Symptom)-[:belongs_to]->(dept:Department)
WHERE d.name = "高血压"
RETURN path LIMIT 10
```

### 2. 聚合查询

```cypher
// 统计每个疾病的症状数量
MATCH (d:Disease)-[:has_symptom]->(s:Symptom)
RETURN d.name, count(s) as symptom_count
ORDER BY symptom_count DESC
LIMIT 10

// 统计每个疾病的药品数量
MATCH (d:Disease)-[:common_drug]->(drug:Drug)
RETURN d.name, count(drug) as drug_count
ORDER BY drug_count DESC
LIMIT 10
```

### 3. 全文搜索

```cypher
// 搜索包含特定关键词的疾病
MATCH (d:Disease)
WHERE d.name CONTAINS "高" OR d.desc CONTAINS "血压"
RETURN d.name, d.desc
LIMIT 10
```

## 📋 常用查询模板

### 1. 疾病信息查询模板

```cypher
// 查询疾病基本信息
MATCH (d:Disease {name: "疾病名称"})
RETURN d.name as 疾病名称,
       d.desc as 疾病描述,
       d.cure_department as 治疗科室,
       d.cure_way as 治疗方法,
       d.symptom as 症状,
       d.cause as 病因,
       d.prevent as 预防措施
```

### 2. 关系查询模板

```cypher
// 查询疾病的所有关系
MATCH (d:Disease {name: "疾病名称"})-[r]-(n)
RETURN type(r) as 关系类型, 
       labels(n) as 目标节点类型,
       n.name as 目标节点名称
```

### 3. 统计查询模板

```cypher
// 统计数据库概览
MATCH (n)
RETURN labels(n) as 节点类型, count(n) as 数量
ORDER BY 数量 DESC
```

## 🎯 实用技巧

### 1. 性能优化

```cypher
// 使用索引查询（如果已创建索引）
MATCH (d:Disease) WHERE d.name = "高血压" RETURN d

// 限制结果数量
MATCH (n) RETURN n LIMIT 100
```

### 2. 数据导出

```cypher
// 导出疾病数据为JSON格式
MATCH (d:Disease)
RETURN d.name, d.desc, d.symptom, d.cause, d.prevent
LIMIT 100
```

### 3. 数据验证

```cypher
// 检查数据完整性
MATCH (d:Disease)
WHERE d.name IS NULL OR d.desc IS NULL
RETURN count(d) as 不完整数据数量
```

## 🚀 快速开始

1. **打开Neo4j浏览器**：http://localhost:7474
2. **登录**：用户名 `neo4j`，密码 `password`
3. **在查询框中输入上述命令**
4. **点击运行按钮执行查询**
5. **查看结果和可视化图表**

## 📊 示例查询结果

运行这些命令后，您将看到：
- 节点和关系的统计信息
- 疾病、症状、药品的具体数据
- 知识图谱的可视化展示
- JSON格式的结构化数据

## ⚠️ 注意事项

1. **查询性能**：复杂查询可能需要较长时间
2. **结果限制**：使用 `LIMIT` 限制结果数量
3. **数据格式**：结果以表格和图形两种方式显示
4. **导出功能**：可以导出查询结果为CSV或JSON格式
