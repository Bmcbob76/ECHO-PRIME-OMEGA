"""
Auto-Documentation System
Automatically generates documentation from code and system state

Authority Level: 11.0
Commander Bobby Don McWilliams II
"""

import logging
import ast
import inspect
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import json

logger = logging.getLogger(__name__)

class AutoDocumentation:
    """Generate documentation automatically from code"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get('docs_output', 'docs'))
        self.output_dir.mkdir(exist_ok=True)
        
        # Documentation templates
        self.templates = self._load_templates()
        
        logger.info(f"Auto-Documentation initialized (output: {self.output_dir})")
    
    def _load_templates(self) -> Dict[str, str]:
        """Load documentation templates"""
        return {
            'module': """# {name}

{description}

## Overview
{overview}

## Classes
{classes}

## Functions
{functions}

## Usage
{usage}

---
*Generated on {timestamp}*
""",
            'class': """### {name}

{description}

**Methods:**
{methods}
""",
            'function': """#### {name}

```python
{signature}
```

{description}

**Parameters:**
{parameters}

**Returns:**
{returns}
"""
        }
    
    def analyze_module(self, module_path: Path) -> Dict[str, Any]:
        """Analyze Python module and extract documentation info"""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            module_info = {
                'name': module_path.stem,
                'path': str(module_path),
                'docstring': ast.get_docstring(tree) or "No description",
                'classes': [],
                'functions': [],
                'imports': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._analyze_class(node)
                    module_info['classes'].append(class_info)
                elif isinstance(node, ast.FunctionDef):
                    # Only top-level functions
                    if isinstance(node, ast.FunctionDef) and \
                       isinstance(getattr(node, 'parent', None), ast.Module):
                        func_info = self._analyze_function(node)
                        module_info['functions'].append(func_info)
            
            return module_info
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze {module_path}: {e}")
            return {}
    
    def _analyze_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Analyze class definition"""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "No description",
            'methods': [],
            'bases': [base.id for base in node.bases if isinstance(base, ast.Name)]
        }
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._analyze_function(item)
                class_info['methods'].append(method_info)
        
        return class_info
    
    def _analyze_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Analyze function definition"""
        func_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "No description",
            'parameters': [],
            'returns': None
        }
        
        # Extract parameters
        for arg in node.args.args:
            param = {'name': arg.arg}
            if arg.annotation:
                param['type'] = ast.unparse(arg.annotation)
            func_info['parameters'].append(param)
        
        # Extract return type
        if node.returns:
            func_info['returns'] = ast.unparse(node.returns)
        
        return func_info
    
    def generate_module_docs(self, module_info: Dict[str, Any]) -> str:
        """Generate markdown documentation for module"""
        # Format classes
        classes_md = ""
        for cls in module_info.get('classes', []):
            methods_md = ""
            for method in cls['methods']:
                params = ", ".join([p['name'] for p in method['parameters']])
                methods_md += f"- `{method['name']}({params})`: {method['docstring']}\n"
            
            classes_md += self.templates['class'].format(
                name=cls['name'],
                description=cls['docstring'],
                methods=methods_md or "No methods"
            )
        
        # Format functions
        functions_md = ""
        for func in module_info.get('functions', []):
            params_md = ""
            for param in func['parameters']:
                param_type = param.get('type', 'Any')
                params_md += f"- `{param['name']}` ({param_type})\n"
            
            functions_md += self.templates['function'].format(
                name=func['name'],
                signature=f"def {func['name']}(...)",
                description=func['docstring'],
                parameters=params_md or "No parameters",
                returns=func.get('returns', 'None')
            )
        
        # Generate full module documentation
        docs = self.templates['module'].format(
            name=module_info['name'],
            description=module_info.get('docstring', 'No description'),
            overview=f"Module: {module_info['name']}",
            classes=classes_md or "No classes",
            functions=functions_md or "No functions",
            usage="See function and class documentation above",
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        return docs
    
    def generate_project_docs(self, project_path: Path) -> Dict[str, str]:
        """Generate documentation for entire project"""
        docs = {}
        
        # Find all Python files
        python_files = list(project_path.rglob('*.py'))
        
        logger.info(f"📚 Generating docs for {len(python_files)} files")
        
        for py_file in python_files:
            if '__pycache__' in str(py_file):
                continue
            
            module_info = self.analyze_module(py_file)
            if module_info:
                module_docs = self.generate_module_docs(module_info)
                docs[module_info['name']] = module_docs
        
        return docs
    
    def save_documentation(self, docs: Dict[str, str]):
        """Save generated documentation to files"""
        for module_name, content in docs.items():
            output_file = self.output_dir / f"{module_name}.md"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"✅ Saved docs: {output_file}")
            except Exception as e:
                logger.error(f"❌ Failed to save {output_file}: {e}")
    
    def generate_system_state_docs(self, system_state: Dict[str, Any]) -> str:
        """Generate documentation for current system state"""
        doc = f"""# Master Launcher System State

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
Current state of the Master Launcher Ultimate system.

## Active Servers
"""
        
        if 'servers' in system_state:
            for server_name, server_data in system_state['servers'].items():
                doc += f"""
### {server_name}
- **Status:** {server_data.get('status', 'unknown')}
- **Port:** {server_data.get('port', 'N/A')}
- **Uptime:** {server_data.get('uptime', 'N/A')}
- **Health:** {server_data.get('health', 'N/A')}
"""
        
        doc += "\n## System Metrics\n"
        
        if 'metrics' in system_state:
            metrics = system_state['metrics']
            doc += f"""
- **CPU Usage:** {metrics.get('cpu', 'N/A')}%
- **Memory Usage:** {metrics.get('memory', 'N/A')}%
- **Disk Usage:** {metrics.get('disk', 'N/A')}%
"""
        
        return doc
    
    def generate_api_docs(self, api_routes: List[Dict[str, Any]]) -> str:
        """Generate API documentation"""
        doc = """# API Documentation

## Endpoints

"""
        
        for route in api_routes:
            doc += f"""
### {route['method']} {route['path']}

{route.get('description', 'No description')}

**Parameters:**
{self._format_parameters(route.get('parameters', []))}

**Response:**
```json
{route.get('response_example', '{}')}
```

---
"""
        
        return doc
    
    def _format_parameters(self, parameters: List[Dict]) -> str:
        """Format parameter list"""
        if not parameters:
            return "No parameters\n"
        
        result = ""
        for param in parameters:
            required = "Required" if param.get('required') else "Optional"
            result += f"- `{param['name']}` ({param.get('type', 'string')}) - {required}\n"
            if 'description' in param:
                result += f"  {param['description']}\n"
        
        return result
    
    def generate_index(self, docs: Dict[str, str]) -> str:
        """Generate documentation index"""
        index = f"""# Master Launcher Ultimate - Documentation Index

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Modules

"""
        
        for module_name in sorted(docs.keys()):
            index += f"- [{module_name}]({module_name}.md)\n"
        
        index += """
## Quick Links

- [Getting Started](START_HERE.md)
- [Configuration](config.yaml)
- [API Documentation](api.md)
- [System State](system_state.md)
"""
        
        return index
    
    def run_full_documentation(self, project_path: Path):
        """Generate complete documentation suite"""
        logger.info("📚 Starting full documentation generation")
        
        # Generate module docs
        docs = self.generate_project_docs(project_path)
        
        # Save module docs
        self.save_documentation(docs)
        
        # Generate and save index
        index = self.generate_index(docs)
        index_file = self.output_dir / "INDEX.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index)
        
        logger.info(f"✅ Documentation complete: {len(docs)} modules documented")
        logger.info(f"📁 Output directory: {self.output_dir}")


if __name__ == "__main__":
    # Test auto-documentation
    config = {'docs_output': 'docs'}
    
    generator = AutoDocumentationGenerator(config)
    
    # Generate docs for current project
    project_root = Path(__file__).parent.parent
    generator.run_full_documentation(project_root)
