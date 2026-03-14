from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch


ARTIFACTS_DIR = Path("artifacts")


def make_figure():
    graph = nx.DiGraph()

    controller = "Controller: Generative Model"
    plant = "Plant: Biological Body's\nAllostatic State"
    setpoint = "Setpoint\n$\\Phi_0 = 2/3$"
    precision = "Coupling Precision\n$\\Phi_{voi}$"

    graph.add_nodes_from([controller, plant, setpoint, precision])
    graph.add_edge(controller, plant)
    graph.add_edge(plant, controller)
    graph.add_edge(setpoint, controller)

    positions = {
        setpoint: (0.5, 0.88),
        controller: (0.5, 0.63),
        plant: (0.5, 0.28),
        precision: (0.5, 0.06),
    }

    fig, ax = plt.subplots(figsize=(10.5, 6.5))

    blanket = FancyBboxPatch(
        (0.14, 0.16),
        0.72,
        0.60,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor="#f2f6ff",
        edgecolor="#1f4e79",
        linewidth=1.8,
        linestyle="-",
        zorder=0,
    )
    ax.add_patch(blanket)
    ax.text(
        0.86,
        0.77,
        "Markov Blanket",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=11,
        color="#1f4e79",
        fontweight="bold",
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=[controller],
        node_color="#7fc8f8",
        node_shape="s",
        node_size=7800,
        ax=ax,
        edgecolors="#0f3d5e",
        linewidths=1.4,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=[plant],
        node_color="#9be7a7",
        node_shape="s",
        node_size=8700,
        ax=ax,
        edgecolors="#145a32",
        linewidths=1.4,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=[setpoint],
        node_color="#fff3cd",
        node_shape="o",
        node_size=2800,
        ax=ax,
        edgecolors="#7d6608",
        linewidths=1.2,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=[precision],
        node_color="#f8f9fa",
        node_shape="o",
        node_size=3200,
        ax=ax,
        edgecolors="#495057",
        linewidths=1.2,
    )

    nx.draw_networkx_labels(graph, positions, font_size=10, font_weight="bold", ax=ax)

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=[(controller, plant)],
        arrowstyle="-|>",
        arrowsize=20,
        width=2.2,
        edge_color="#145a32",
        connectionstyle="arc3,rad=-0.05",
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=[(plant, controller)],
        arrowstyle="-|>",
        arrowsize=20,
        width=2.2,
        edge_color="#0f3d5e",
        connectionstyle="arc3,rad=-0.05",
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=[(setpoint, controller)],
        arrowstyle="-|>",
        arrowsize=18,
        width=1.8,
        edge_color="#7d6608",
        ax=ax,
    )

    ax.text(
        0.57,
        0.50,
        "Control signal:\nEfferent autonomic drive",
        fontsize=9.5,
        color="#145a32",
        ha="left",
        va="center",
        transform=ax.transAxes,
        bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "alpha": 0.82},
    )
    ax.text(
        0.57,
        0.40,
        "Feedback:\nInteroceptive afference",
        fontsize=9.5,
        color="#0f3d5e",
        ha="left",
        va="center",
        transform=ax.transAxes,
        bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "alpha": 0.82},
    )

    ax.set_title("Figure 4: The HST Architecture", fontsize=14, fontweight="bold")
    ax.set_xlim(0.06, 0.94)
    ax.set_ylim(0.0, 0.98)
    ax.axis("off")

    plt.tight_layout()
    return fig


def main():
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    output_path = ARTIFACTS_DIR / "figure4_hst_architecture.png"

    fig = make_figure()
    fig.savefig(output_path, dpi=220)
    print(f"Saved figure: {output_path}")

    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    main()