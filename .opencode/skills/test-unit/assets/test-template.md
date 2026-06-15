# 单元测试生成规则说明

## 生成策略

### 函数分类

根据函数特征自动选择合适的测试模板：

1. **纯函数**（无参数）
   - 测试正常返回值
   - 测试幂等性

2. **带参数函数**
   - 正常值测试
   - 边界值测试（空值、0、None）
   - 非法值测试（类型错误、范围错误）

3. **返回布尔值**
   - True 场景
   - False 场景

4. **返回集合（list/dict）**
   - 非空检查
   - 元素类型检查
   - 数量检查

5. **可能抛出异常**
   - 正常参数不抛异常
   - 非法参数抛出指定异常

## 需要手动补充的部分

生成的测试文件中标记为 `TODO` 的地方需要人工完善：

- 具体的预期值（如断言的具体数值）
- 业务相关的边界条件
- Mock 外部依赖（数据库、API）
- 复杂的参数组合

## 示例

### 输入

```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """计算折扣后价格"""
    if price < 0:
        raise ValueError("价格不能为负数")
    if discount_rate < 0 or discount_rate > 1:
        raise ValueError("折扣率必须在0-1之间")
    return price * (1 - discount_rate)
```

### 输出

```python
class TestCalculateDiscount:
    def test_calculate_discount_success(self):
        result = calculate_discount(100.0, 0.2)
        assert result is not None
        assert isinstance(result, float)

    def test_calculate_discount_empty_values(self):
        result = calculate_discount(0.0, 0.0)
        # TODO: 根据业务逻辑补充断言

    def test_calculate_discount_invalid_input(self):
        with pytest.raises((ValueError, TypeError)):
            calculate_discount(None, None)
```

**需要补充**：
- `test_success`: 具体断言 `assert result == 80.0`
- `test_empty`: 业务逻辑（0价格是否允许？）
- `test_invalid`: 分别测试 price<0 和 discount_rate 越界
