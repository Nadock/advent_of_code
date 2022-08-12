package day12

import (
	"log"
	"strings"

	"2021.advent-of-code.rileychase.net/internal"
)

func day12part1(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	g := newGraph(lines)
	log.Printf("%+v", g)

	return 0, nil
}

type graph struct {
	nodes map[string]bool
	edges map[string]string
}

func newGraph(paths []string) *graph {
	g := &graph{nodes: make(map[string]bool), edges: make(map[string]string)}
	for _, path := range paths {
		names := strings.Split(path, "-")
		start, end := names[0], names[1]
		g.addNode(start)
		g.addNode(end)
		g.addEdge(start, end)
		g.addEdge(end, start)
	}
	return g
}

func (g *graph) addEdge(start, end string) {
	g.edges[start] = end
}

func (g *graph) addNode(name string) {
	if name == "start" || name == "end" || strings.ToLower(name) != name {
		g.nodes[name] = false
	} else {
		g.nodes[name] = true
	}
}

// Return all the paths from the start node to the end node that obey the small/large rule
func (g *graph) findAllPaths() *[][]string {

	visited := make(map[string]bool)
	root := "start"

	return g.search(root, &visited)
}

func (g *graph) search(node string, visited *map[string]bool, path *[]string) *[]string {
	if node == "end" {
		return path
	} else if (*visited)[node] && !g.nodes[node] {
		return nil
	}

}
