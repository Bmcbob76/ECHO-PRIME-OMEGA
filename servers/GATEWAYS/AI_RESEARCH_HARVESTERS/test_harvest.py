#!/usr/bin/env python3
"""
Quick test of AI Research Harvesters - FULL PRODUCTION
Tests arXiv harvesting and EKM generation
"""

import sys
import asyncio
sys.path.insert(0, r'P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\AI_RESEARCH_HARVESTERS')

from ai_research_harvesters_mcp import AIResearchHarvester

async def test_harvest():
    """Test real arXiv harvesting"""
    print("=" * 80)
    print("AI RESEARCH HARVESTERS - PRODUCTION TEST")
    print("=" * 80)
    
    harvester = AIResearchHarvester()
    
    # Test with a simple query
    print("\n🔍 Testing arXiv harvest: 'transformer attention'")
    print("Requesting 5 recent papers...\n")
    
    papers = await harvester.harvest_arxiv("transformer attention", max_results=5)
    
    print(f"\n✅ Harvested {len(papers)} papers")
    
    if papers:
        print("\n📄 Sample paper:")
        paper = papers[0]
        print(f"  Title: {paper.title[:80]}...")
        print(f"  Authors: {', '.join(paper.authors[:3])}")
        print(f"  arXiv ID: {paper.arxiv_id}")
        print(f"  Categories: {', '.join(paper.categories)}")
        
        print("\n🧠 Generating EKM with AI-ML analysis...")
        ekm_info = harvester.generate_ekm(paper)
        
        if ekm_info:
            print(f"\n✅ EKM Generated:")
            print(f"  File: {ekm_info['file']}")
            print(f"  Tier: {ekm_info['tier']}")
            print(f"  Size: {ekm_info['size']} chars")
        else:
            print("❌ EKM generation failed")
    else:
        print("❌ No papers found")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_harvest())
